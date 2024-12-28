from django.urls import path
from .views import ExportProductsView,ProductListCreateView,ProductDetailView,ProductDisableView,\
    UserRegistrationView,LoginView



urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/export/', ExportProductsView.as_view(), name='product-export'),
    path('products/<int:pk>/disable/', ProductDisableView.as_view(), name='product-disable'),
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('auth/login/', LoginView.as_view(), name='user-login'),

]
