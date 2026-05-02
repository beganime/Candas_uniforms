# Generated manually for Cadas Uniforms
from django.db import migrations, models
import django.db.models.deletion
import catalog.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='Название категории')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=160, unique=True, verbose_name='URL')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to=catalog.models.upload_to_categories, verbose_name='Изображение')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
                ('sort_order', models.PositiveIntegerField(default=100, verbose_name='Порядок')),
            ],
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории', 'ordering': ['sort_order', 'title']},
        ),
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(choices=[('home', 'Главная'), ('about', 'О компании')], max_length=30, unique=True, verbose_name='Страница')),
                ('title', models.CharField(max_length=180, verbose_name='Заголовок')),
                ('subtitle', models.CharField(blank=True, max_length=240, verbose_name='Подзаголовок')),
                ('body', models.TextField(blank=True, verbose_name='Текст страницы')),
                ('hero_image', models.ImageField(blank=True, null=True, upload_to=catalog.models.upload_to_pages, verbose_name='Главное изображение')),
                ('second_image', models.ImageField(blank=True, null=True, upload_to=catalog.models.upload_to_pages, verbose_name='Дополнительное изображение')),
                ('phone', models.CharField(blank=True, max_length=80, verbose_name='Телефон на странице')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email на странице')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес на странице')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={'verbose_name': 'Редактируемая страница', 'verbose_name_plural': 'Редактируемые страницы'},
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='Cadas Uniforms', max_length=120, verbose_name='Название сайта')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=catalog.models.upload_to_site, verbose_name='Логотип')),
                ('phone', models.CharField(blank=True, max_length=80, verbose_name='Телефон')),
                ('second_phone', models.CharField(blank=True, max_length=80, verbose_name='Дополнительный телефон')),
                ('whatsapp', models.CharField(blank=True, help_text='Например: +99361234567', max_length=80, verbose_name='WhatsApp')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('instagram', models.URLField(blank=True, verbose_name='Instagram')),
                ('telegram', models.URLField(blank=True, verbose_name='Telegram')),
                ('domain', models.URLField(default='https://medisinskayaodezhda.ru', verbose_name='Домен сайта')),
                ('hero_badge', models.CharField(default='Медицинская одежда для клиник, салонов и специалистов', max_length=160, verbose_name='Короткая фраза в шапке')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={'verbose_name': 'Настройки сайта', 'verbose_name_plural': 'Настройки сайта'},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=180, verbose_name='Название товара')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=220, unique=True, verbose_name='URL')),
                ('sku', models.CharField(blank=True, max_length=80, verbose_name='Артикул')),
                ('short_description', models.CharField(blank=True, max_length=260, verbose_name='Короткое описание')),
                ('description', models.TextField(blank=True, verbose_name='Полное описание')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Цена')),
                ('old_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Старая цена')),
                ('currency', models.CharField(default='₽', max_length=20, verbose_name='Валюта')),
                ('sizes', models.CharField(blank=True, help_text='Например: XS, S, M, L, XL', max_length=160, verbose_name='Размеры')),
                ('colors', models.CharField(blank=True, max_length=180, verbose_name='Цвета')),
                ('material', models.CharField(blank=True, max_length=180, verbose_name='Материал')),
                ('care', models.CharField(blank=True, max_length=220, verbose_name='Уход')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to=catalog.models.upload_to_products, verbose_name='Главное фото')),
                ('qr_code', models.ImageField(blank=True, editable=False, null=True, upload_to=catalog.models.upload_to_qr, verbose_name='QR-код товара')),
                ('is_active', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Показывать на главной')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлён')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='catalog.category', verbose_name='Категория')),
            ],
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары', 'ordering': ['-is_featured', '-created_at']},
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=catalog.models.upload_to_products, verbose_name='Фото')),
                ('alt', models.CharField(blank=True, max_length=160, verbose_name='Alt-текст')),
                ('sort_order', models.PositiveIntegerField(default=100, verbose_name='Порядок')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='catalog.product', verbose_name='Товар')),
            ],
            options={'verbose_name': 'Фото товара', 'verbose_name_plural': 'Фото товара', 'ordering': ['sort_order', 'id']},
        ),
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_type', models.CharField(choices=[('product_order', 'Заявка по товару'), ('general', 'Общее сообщение')], default='general', max_length=30, verbose_name='Тип заявки')),
                ('name', models.CharField(max_length=120, verbose_name='Имя')),
                ('phone', models.CharField(max_length=80, verbose_name='Телефон')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Email')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Город / адрес')),
                ('message', models.TextField(blank=True, verbose_name='Комментарий')),
                ('source_page', models.CharField(blank=True, max_length=500, verbose_name='Страница-источник')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP-адрес')),
                ('user_agent', models.TextField(blank=True, verbose_name='User-Agent / устройство')),
                ('is_processed', models.BooleanField(default=False, verbose_name='Обработано')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата заявки')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requests', to='catalog.product', verbose_name='Товар')),
            ],
            options={'verbose_name': 'Заявка клиента', 'verbose_name_plural': 'Заявки клиентов', 'ordering': ['-created_at']},
        ),
    ]
