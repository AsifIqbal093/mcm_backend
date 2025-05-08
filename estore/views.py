from rest_framework import viewsets ,filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUserRole, IsAdminOrReadOnly
from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer
from django_filters.rest_framework import DjangoFilterBackend
from user.models import User
from user.serializers import ClientSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand', 'category']
    search_fields = ['product_name', 'category__name']
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='user')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]  
