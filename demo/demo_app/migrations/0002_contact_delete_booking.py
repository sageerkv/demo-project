# Generated by Django 4.1.7 on 2023-05-09 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=255)),
                ('c_email', models.EmailField(max_length=254)),
                ('c_subject', models.CharField(max_length=300)),
                ('c_text_area', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
    ]
