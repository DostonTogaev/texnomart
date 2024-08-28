from django.contrib import admin
from texnomart.models import Category, Images, Product, Comment, Attribute, Attribute_key, Attribute_Value

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Images)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name']

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'rating' ]


admin.site.register(Attribute_key)
admin.site.register(Attribute_Value)
admin.site.register(Attribute)
