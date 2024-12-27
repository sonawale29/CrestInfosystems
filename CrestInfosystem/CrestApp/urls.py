from django.urls import path
from .views import ProductListCreateView, ProductDetailView,ProductExportView,RegisterView,\
    LoginView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/export/', ProductExportView.as_view(), name='product-export'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
