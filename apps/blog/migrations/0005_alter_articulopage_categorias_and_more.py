# Generated by Django 4.1.8 on 2023-04-23 16:13

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('blog', '0004_rename_articulolistingpage_articuloslistingpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulopage',
            name='categorias',
            field=modelcluster.fields.ParentalManyToManyField(to='blog.categoria'),
        ),
        migrations.AlterField(
            model_name='articulopage',
            name='imagen',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='portada', to='wagtailimages.image'),
        ),
    ]