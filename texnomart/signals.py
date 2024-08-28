import json
import os
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from texnomart.models import Product, Category
from config.settings import BASE_DIR
from django.core.cache import cache
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User  
from django.core.mail import send_mail



@receiver([post_save, pre_delete], sender=Product)
@receiver([post_save, pre_delete], sender=Category)
def handle_product_category_signals(sender, instance, **kwargs):
    signal_type = kwargs.get('signal')

    if signal_type == post_save:
        if kwargs.get('created', False):
            file_path = os.path.join(BASE_DIR, 'texnomart/delete_texno/', f'texnomart{instance.id}.json')
            data = {
                'id': instance.id,
                'name': instance.name if sender == Product else instance.title,
                'slug': instance.slug,
            }
            with open(file_path, mode='w') as file_json:
                json.dump(data, file_json, indent=4)
            print(f'{instance.name if sender == Product else instance.title} created and saved to JSON!')

        else:
            print(f'{instance.name if sender == Product else instance.title} updated!')

    elif signal_type == pre_delete:
        file_path = os.path.join(BASE_DIR, 'texnomart/delete_texno/', f'texnomart{instance.id}.json')
        data = {
            'id': instance.id,
            'name': instance.name if sender == Product else instance.title,
            'slug': instance.slug,
        }
        with open(file_path, mode='w') as file_json:
            json.dump(data, file_json, indent=4)
        print(f'{instance.name if sender == Product else instance.title} is deleted and saved to JSON!')

@receiver(post_save, sender=Product)
@receiver(pre_save, sender=Product)
@receiver(post_save, sender=Category)
@receiver(pre_save, sender=Category)
def clear_cache_post_data(sender, instance, **kwargs):
    cache.delete('category_list')
    slug = instance.slug
    cache.delete(f'product_detail_{slug}')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



@receiver(post_save, sender=Product)
@receiver(post_save, sender=Category)
def send_notification_email(sender, instance, created, **kwargs):
        if created:
            if sender == Product:
                subject = 'Yangi mahsulot yaratildi'
                message = f'Yangi mahsulot yaratildi: {instance.name}'  
            elif sender == Category:
                subject = 'Yangi kategoriya yaratildi'
                message = f'Yangi kategoriya yaratildi: {instance.title}'  
            
        
        recipient_list = User.objects.values_list('email', flat=True)

        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

@receiver(post_delete, sender=Product)
@receiver(post_delete, sender=Category)
def send_notification_on_delete(sender, instance, **kwargs):
    if sender == Product:
        subject = 'Mahsulot o\'chirildi'
        message = f'Mahsulot o\'chirildi: {instance.name}'  
    elif sender == Category:
        subject = 'Kategoriyangiz o\'chirildi'
        message = f'Kategoriya o\'chirildi: {instance.title}'  

    recipient_list = User.objects.values_list('email', flat=True)
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)