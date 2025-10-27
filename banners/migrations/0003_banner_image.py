# Generated manually to add image field to Banner

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0002_simplify_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='banners/', verbose_name='Imagem'),
        ),
    ]

