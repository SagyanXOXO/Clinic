# Generated by Django 3.2.6 on 2021-09-11 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Misc', '0006_blog_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='like',
            new_name='views',
        ),
    ]