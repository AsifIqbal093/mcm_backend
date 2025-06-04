from rest_framework import viewsets ,filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsAdminUserRole, IsAdminOrReadOnly
from .models import Product, Category, Brand
from .serializers import *
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
    search_fields = [
        'product_name',
        'SKU',
        'status',
        'category__name',
        'brand__brand_name'
    ]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrReadOnly()]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'sub_categories']

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


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SubCategorySerializer

    def get_queryset(self):
        if self.action == 'list':
            return SubCategory.objects.filter(parent=None)
        return SubCategory.objects.all()
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='paginate', type=bool, location=OpenApiParameter.QUERY,
                            description="Set to false to disable pagination")
        ]
    )
    def list(self, request, *args, **kwargs):
        if request.query_params.get('paginate') == 'false':
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
