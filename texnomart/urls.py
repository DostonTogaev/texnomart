from django.contrib import admin
from django.urls import path
from texnomart.views.category.category_views import CategoryListApi, CategoryDetail, CategoryAddApiView, CategoryUpdateApiView, CategoryDeleteApiView
from texnomart.views.product.product_view import ProductDetailApiView, ProductEditApiView, ProductDeleteApiView, AttributeKey, AttributeValue, ProductADDApiView, ProductListApiView
from texnomart.views.auth import auth_view
from texnomart import custom_token, cutom_obtain_views


urlpatterns = [
    #Category
    path('categories/', CategoryListApi.as_view(), name='category-list'),
    path('category/<slug:category_slug>/', ProductListApiView.as_view()),
    path('category/add-category/', CategoryAddApiView.as_view(), name='category-add'),
    path('category/<slug:slug>/delete/',CategoryDeleteApiView.as_view()),
    path('category/<slug:slug>/edit/', CategoryUpdateApiView.as_view()),

    #Product
    path('product/detail/<slug:slug>/', ProductDetailApiView.as_view()),
    path('product/<int:id>/edit/', ProductEditApiView.as_view()),
    path('product/<int:id>/delete/', ProductDeleteApiView.as_view()),
    path('product/add/',ProductADDApiView.as_view()),

    #Attribute
    path('attribute-key/', AttributeKey.as_view()),
    path('attribute-value/', AttributeValue.as_view()),

    path('api-token-auth/', custom_token.CustomAuthToken.as_view()),
    path('api/token/', cutom_obtain_views.MyTokenObtain.as_view(), name='token_obtain_pair'),
    path('logout/', cutom_obtain_views.LogoutAPIView.as_view()),
    #path('register/', cutom_obtain_views.RegisterAPIView.as_view()),

    path('login/', auth_view.UserLoginAPIView.as_view()),
    path('register/', auth_view.UserRegisterAPIView.as_view()),
    #path('logout/', auth_view.UserLogoutAPIView.as_view()),

    #path('send-email', EmailAPI.as_view()),


   

]