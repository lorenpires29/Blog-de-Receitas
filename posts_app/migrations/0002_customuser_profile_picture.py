# Generated by Django 5.0.3 on 2024-03-19 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
