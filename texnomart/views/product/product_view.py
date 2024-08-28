from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView, CreateAPIView, RetrieveAPIView
from texnomart.serializer import ProductSerializer, Attribute_KeySerializer, Attribute_ValueSerializer
from texnomart.models import Product, Attribute_key, Attribute_Value
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status 

class ProductListApiView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        queryset = Product.objects.filter(category__slug = category_slug)
        
        return queryset
    
class ProductDetailApiView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    lookup_field='slug'

    
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        cache_key = f'product_detail_{slug}'
        product_data = cache.get(cache_key)

        if not product_data:
            try:
                product = Product.objects.get(slug=slug)
                serializer = self.get_serializer(product, context={'request': request})
                product_data = serializer.data
                cache.set(cache_key, product_data, timeout=60)
            except Product.DoesNotExist:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(product_data)





class ProductEditApiView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field='id'


class ProductDeleteApiView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]

    lookup_field='id'

class ProductADDApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AttributeKey(ListAPIView):
    queryset = Attribute_key.objects.all()
    serializer_class = Attribute_KeySerializer


class AttributeValue(ListAPIView):
    queryset = Attribute_Value.objects.all()
    serializer_class = Attribute_KeySerializer