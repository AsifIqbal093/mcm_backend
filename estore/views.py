from rest_framework import viewsets ,filters
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminUserRole, IsAdminOrReadOnly
from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer
from django_filters.rest_framework import DjangoFilterBackend
from user.models import User
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand', 'category', 'status']
    search_fields = ['product_name', 'category__name']
    

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='all_data',
                description='Set to true to retrieve all data without pagination',
                required=False,
                type=bool
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        all_data = request.query_params.get('all_data', '').lower() == 'true'
        queryset = self.filter_queryset(self.get_queryset())

        if all_data:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        
        return super().list(request, *args, **kwargs)



class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['brand_name']

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='all_data',
                description='Set to true to retrieve all data without pagination',
                required=False,
                type=bool
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        all_data = request.query_params.get('all_data', '').lower() == 'true'
        queryset = self.filter_queryset(self.get_queryset())

        if all_data:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
