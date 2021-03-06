# Generated by Django 3.2.6 on 2021-09-04 07:58

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('Personnel', '0001_initial'),
        ('Misc', '0004_alter_blog_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Personnel.employee'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='thumbnail',
            field=models.FileField(blank=True, null=True, upload_to='blog'),
        ),
    ]
