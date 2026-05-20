from django.db import migrations, models


def create_catalog_page(apps, schema_editor):
    PageContent = apps.get_model('catalog', 'PageContent')
    PageContent.objects.get_or_create(
        key='catalog',
        defaults={
            'title': 'Каталог медицинской одежды',
            'subtitle': 'Подберите форму по категории, цвету, размеру или артикулу.',
            'body': '',
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_homebanner_homestat_promoblock_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagecontent',
            name='key',
            field=models.CharField(
                choices=[('home', 'Главная'), ('catalog', 'Каталог'), ('about', 'О компании')],
                max_length=30,
                unique=True,
                verbose_name='Страница',
            ),
        ),
        migrations.RunPython(create_catalog_page, migrations.RunPython.noop),
    ]
