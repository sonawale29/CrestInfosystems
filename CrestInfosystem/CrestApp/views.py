from rest_framework import generics, filters,status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer
from .utils import generate_excel_file
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, LoginSerializer, TokenSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import IsAdmin, IsUserOrAdmin
from rest_framework.permissions import AllowAny

User = get_user_model()


# Create and List API
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsUserOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'description']
    search_fields = ['title', 'description']
    ordering_fields = ['created_on', 'updated_on']
    ordering = ['-created_on']


# Retrieve, Update, and Delete API
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ExportProductsView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request, *args, **kwargs):
        # Fetch all active products
        products = Product.objects.filter(is_active=True)

        # Generate Excel workbook
        workbook = generate_excel_file(products)

        # Prepare HTTP response with workbook
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="products.xlsx"'

        # Save workbook to response
        workbook.save(response)
        return response


class ProductDisableView(APIView):
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            # Fetch the product by ID
            product = Product.objects.get(pk=pk)

            # Disable the product
            product.is_active = False
            product.save()

            # Return success response
            return Response({"message": "Product disabled successfully."}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            # Return error if product not found
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            token_serializer = TokenSerializer({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
            return Response(token_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

