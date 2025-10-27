# Generated manually to simplify Banner model

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        # Add new fields
        migrations.AddField(
            model_name='banner',
            name='name',
            field=models.CharField(default='Banner', max_length=200, verbose_name='Nome'),
        ),
        migrations.AddField(
            model_name='banner',
            name='link',
            field=models.URLField(blank=True, null=True, verbose_name='Link'),
        ),
        
        # Remove old fields
        migrations.RemoveField(
            model_name='banner',
            name='title',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='description',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='image',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='link_url',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='banner_type',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='position',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='order',
        ),
        
        # Change start_date to non-null
        migrations.AlterField(
            model_name='banner',
            name='start_date',
            field=models.DateTimeField(verbose_name='Data de Início'),
        ),
        
        # Update ordering
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['-start_date'], 'verbose_name': 'Banner', 'verbose_name_plural': 'Banners'},
        ),
    ]

