# Generated by Django 5.1 on 2024-08-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texnomart', '0002_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('position', models.CharField(max_length=16, null=True)),
                ('email', models.CharField(max_length=50, null=True)),
                ('describe', models.TextField(blank=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Consult',
            },
        ),
    ]
