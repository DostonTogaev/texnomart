from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView , RetrieveDestroyAPIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from texnomart.views.auth.auth_view import IsSuperUser
from rest_framework.views import APIView
from rest_framework import status 
from rest_framework.response import Response
from texnomart.models import Category, Product
from texnomart.serializer import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.core.cache import cache
from rest_framework import filters



class CategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'slug']
    search_fields = ['title']

    def get(self, request, *args, **kwargs):
        cache_key = 'category_list'
        cached_data = cache.get(cache_key)
        if cached_data is None:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            cached_data = serializer.data
            cache.set(cache_key, cached_data, timeout=60)
            return Response(cached_data)
        return Response(cached_data)


class CategoryDetail(RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field ='slug'

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        if category is not None:
            return Product.objects.filter(category=category)
        return Product.objects.all()
    
    

class CategoryAddApiView(APIView):
    permission_classes = [IsSuperUser]
    def post(self, request):
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Category successfully created', status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CategoryUpdateApiView(RetrieveUpdateAPIView):  
    permission_classes = [IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'



class CategoryDeleteApiView(RetrieveDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
   