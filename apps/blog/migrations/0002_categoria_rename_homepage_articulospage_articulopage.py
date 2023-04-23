# Generated by Django 4.1.8 on 2023-04-23 11:27

from django.db import migrations, models
import django.db.models.deletion
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('wagtailcore', '0083_workflowcontenttype'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.RenameModel(
            old_name='HomePage',
            new_name='ArticulosPage',
        ),
        migrations.CreateModel(
            name='ArticuloPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('contenido', wagtail.fields.RichTextField(blank=True)),
                ('categorias', models.CharField(max_length=255)),
                ('imagen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portada', to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
