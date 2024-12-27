from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product,User
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
import openpyxl
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create and List API
class ProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'description']
    search_fields = ['title', 'description']
    ordering_fields = ['created_on', 'updated_on']
    ordering = ['-created_on']


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            'access_token': access_token,
        })


# Retrieve, Update, and Delete API
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class ProductExportView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        products = Product.objects.filter(is_active=True)
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Products"

        # Write headers
        headers = ['ID', 'Title', 'Description', 'Price', 'Discount', 'Created On']
        sheet.append(headers)

        # Write product data
        for product in products:
            sheet.append([
                product.id,
                product.title,
                product.description,
                product.price,
                product.discount,
                product.created_on,
            ])

        # Create response
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
        workbook.save(response)
        return response