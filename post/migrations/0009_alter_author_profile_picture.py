# Generated by Django 4.2.15 on 2024-08-19 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0008_alter_author_profile_picture_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_pic.jpg', upload_to=''),
        ),
    ]
