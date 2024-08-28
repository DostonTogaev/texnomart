from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField( blank=True)
    image = models.ImageField(upload_to='media/images/category/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.FloatField()
    slug = models.SlugField(blank=True)
    is_liked = models.ManyToManyField(User, related_name='liked_products', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    created_at = models.DateField(auto_now_add= True)
    updated_at = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    




class Images(models.Model):
    is_primary = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/')
    product = models.ForeignKey('Product',on_delete=models.CASCADE, related_name='images')

class Attribute_key(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Attribute_Value(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    key = models.ForeignKey('Attribute_Key', on_delete=models.CASCADE)
    value= models.ForeignKey('Attribute_Value', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='attributes')

class Comment(models.Model):
    class RatingChoice(models.TextChoices):
        Zero = '0'
        One = 'One'
        Two = 'Two'
        Three = 'Three'
        Four = 'Four'
        Five = 'Five'

    rating = models.CharField(max_length=100, choices=RatingChoice.choices, default=RatingChoice.One.value )
    message = models.TextField()
    file = models.FileField(upload_to='media/comments', null=True, blank=True)
    product = models.ForeignKey('Product', on_delete = models.CASCADE, related_name = 'comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments' )

class Consult(models.Model):
    name = models.CharField(max_length=16)
    position = models.CharField(max_length=16, null=True)
    email = models.CharField(max_length=50, null=True)
    describe = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Consult'