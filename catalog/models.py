from __future__ import annotations

from io import BytesIO

import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from .utils import optimize_image_path


def upload_to_site(instance, filename):
    return f'site/{filename}'


def upload_to_pages(instance, filename):
    return f'pages/{instance.key}/{filename}'


def upload_to_home(instance, filename):
    return f'home/{filename}'


def upload_to_categories(instance, filename):
    return f'categories/{filename}'


def upload_to_products(instance, filename):
    return f'products/{filename}'


def upload_to_qr(instance, filename):
    return f'qr/{filename}'


def unique_slug(instance, source_field: str = 'title') -> str:
    base_value = getattr(instance, source_field, '') or 'item'
    base_slug = slugify(base_value, allow_unicode=True) or 'item'
    slug = base_slug
    model = instance.__class__
    counter = 2
    while model.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
        slug = f'{base_slug}-{counter}'
        counter += 1
    return slug


class SiteSettings(models.Model):
    site_name = models.CharField('Название сайта', max_length=120, default='Cadas Uniforms')
    logo = models.ImageField('Логотип', upload_to=upload_to_site, blank=True, null=True)
    phone = models.CharField('Телефон', max_length=80, blank=True)
    second_phone = models.CharField('Дополнительный телефон', max_length=80, blank=True)
    whatsapp = models.CharField('WhatsApp', max_length=80, blank=True, help_text='Например: +99361234567')
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Адрес', max_length=255, blank=True)
    instagram = models.URLField('Instagram', blank=True)
    telegram = models.URLField('Telegram', blank=True)
    domain = models.URLField('Домен сайта', default='https://medisinskayaodezhda.ru')
    hero_badge = models.CharField('Короткая фраза в шапке', max_length=160, default='Медицинская одежда для клиник, салонов и специалистов')
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.logo and hasattr(self.logo, 'path'):
            optimize_image_path(self.logo.path)

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj:
            return obj
        return cls.objects.create(site_name='Cadas Uniforms', domain=getattr(settings, 'SITE_DOMAIN', 'https://medisinskayaodezhda.ru'))


class PageContent(models.Model):
    HOME = 'home'
    CATALOG = 'catalog'
    ABOUT = 'about'
    PAGE_CHOICES = [
        (HOME, 'Главная'),
        (CATALOG, 'Каталог'),
        (ABOUT, 'О компании'),
    ]

    key = models.CharField('Страница', max_length=30, choices=PAGE_CHOICES, unique=True)
    title = models.CharField('Заголовок', max_length=180)
    subtitle = models.CharField('Подзаголовок', max_length=240, blank=True)
    body = models.TextField('Текст страницы', blank=True)
    hero_image = models.ImageField('Главное изображение', upload_to=upload_to_pages, blank=True, null=True)
    second_image = models.ImageField('Дополнительное изображение', upload_to=upload_to_pages, blank=True, null=True)
    phone = models.CharField('Телефон на странице', max_length=80, blank=True)
    email = models.EmailField('Email на странице', blank=True)
    address = models.CharField('Адрес на странице', max_length=255, blank=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Редактируемая страница'
        verbose_name_plural = 'Редактируемые страницы'

    def __str__(self):
        return self.get_key_display()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for image_field in [self.hero_image, self.second_image]:
            if image_field and hasattr(image_field, 'path'):
                optimize_image_path(image_field.path)


class Category(models.Model):
    title = models.CharField('Название категории', max_length=120)
    slug = models.SlugField('URL', max_length=160, unique=True, blank=True, allow_unicode=True)
    description = models.TextField('Описание', blank=True)
    image = models.ImageField('Изображение', upload_to=upload_to_categories, blank=True, null=True)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    show_on_home = models.BooleanField('Показывать на главной', default=True)
    sort_order = models.PositiveIntegerField('Порядок', default=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self)
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path'):
            optimize_image_path(self.image.path)

    def get_absolute_url(self):
        return reverse('catalog:catalog') + f'?category={self.slug}'


class Product(models.Model):
    title = models.CharField('Название товара', max_length=180)
    slug = models.SlugField('URL', max_length=220, unique=True, blank=True, allow_unicode=True)
    sku = models.CharField('Артикул', max_length=80, blank=True)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    short_description = models.CharField('Короткое описание', max_length=260, blank=True)
    description = models.TextField('Полное описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2, null=True, blank=True)
    old_price = models.DecimalField('Старая цена', max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField('Валюта', max_length=20, default='₽')
    sizes = models.CharField('Размеры', max_length=160, blank=True, help_text='Например: XS, S, M, L, XL')
    colors = models.CharField('Цвета', max_length=180, blank=True)
    material = models.CharField('Материал', max_length=180, blank=True)
    care = models.CharField('Уход', max_length=220, blank=True)
    badge_text = models.CharField('Бейдж на карточке', max_length=80, blank=True, help_text='Например: НОВИНКА, ХИТ, 50%')
    is_new = models.BooleanField('Новинка', default=False)
    is_best_price = models.BooleanField('Хорошая цена', default=False)
    is_bestseller = models.BooleanField('Хит продаж', default=False)
    main_image = models.ImageField('Главное фото', upload_to=upload_to_products, blank=True, null=True)
    qr_code = models.ImageField('QR-код товара', upload_to=upload_to_qr, blank=True, null=True, editable=False)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    is_featured = models.BooleanField('Показывать на главной', default=False)
    home_sort_order = models.PositiveIntegerField('Порядок на главной', default=100)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['home_sort_order', '-is_featured', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    def get_full_url(self):
        domain = getattr(settings, 'SITE_DOMAIN', 'https://medisinskayaodezhda.ru').rstrip('/')
        try:
            site = SiteSettings.objects.first()
            if site and site.domain:
                domain = site.domain.rstrip('/')
        except Exception:
            pass
        return f'{domain}{self.get_absolute_url()}'

    @property
    def discount_percent(self) -> int | None:
        if not self.price or not self.old_price or self.old_price <= self.price:
            return None
        try:
            return int(round((1 - float(self.price) / float(self.old_price)) * 100))
        except (TypeError, ValueError, ZeroDivisionError):
            return None

    @property
    def card_badge(self) -> str:
        if self.badge_text:
            return self.badge_text
        discount = self.discount_percent
        if discount:
            return f'-{discount}%'
        if self.is_new:
            return 'НОВИНКА'
        if self.is_bestseller:
            return 'ХИТ'
        if self.category:
            return self.category.title
        return ''

    def _build_qr(self):
        qr_img = qrcode.make(self.get_full_url())
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        file_name = f'product-{self.pk}.png'
        self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)
        Product.objects.filter(pk=self.pk).update(qr_code=self.qr_code.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self)
        super().save(*args, **kwargs)
        if self.main_image and hasattr(self.main_image, 'path'):
            optimize_image_path(self.main_image.path)
        if self.pk and not self.qr_code:
            self._build_qr()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField('Фото', upload_to=upload_to_products)
    alt = models.CharField('Alt-текст', max_length=160, blank=True)
    sort_order = models.PositiveIntegerField('Порядок', default=100)

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товара'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.alt or f'Фото: {self.product}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path'):
            optimize_image_path(self.image.path)


class HomeBanner(models.Model):
    title = models.CharField('Заголовок баннера', max_length=180)
    subtitle = models.CharField('Подзаголовок', max_length=260, blank=True)
    badge = models.CharField('Маленькая надпись сверху', max_length=120, blank=True)
    image = models.ImageField('Фото баннера', upload_to=upload_to_home, blank=True, null=True)
    button_text = models.CharField('Текст основной кнопки', max_length=80, default='Смотреть каталог')
    button_url = models.CharField('Ссылка основной кнопки', max_length=220, default='/catalog/')
    second_button_text = models.CharField('Текст второй кнопки', max_length=80, blank=True)
    second_button_url = models.CharField('Ссылка второй кнопки', max_length=220, blank=True)
    is_active = models.BooleanField('Показывать', default=True)
    sort_order = models.PositiveIntegerField('Порядок', default=100)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Баннер главной'
        verbose_name_plural = 'Баннеры главной'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path'):
            optimize_image_path(self.image.path)


class HomeStat(models.Model):
    value = models.CharField('Число / значение', max_length=40)
    label = models.CharField('Подпись', max_length=120)
    is_active = models.BooleanField('Показывать', default=True)
    sort_order = models.PositiveIntegerField('Порядок', default=100)

    class Meta:
        verbose_name = 'Цифра на главной'
        verbose_name_plural = 'Цифры на главной'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return f'{self.value} — {self.label}'


class PromoBlock(models.Model):
    title = models.CharField('Заголовок акции', max_length=140)
    subtitle = models.CharField('Подпись', max_length=180, blank=True)
    accent_text = models.CharField('Крупный акцент', max_length=40, blank=True, help_text='Например: 50%, NEW, SALE')
    image = models.ImageField('Фото / фон акции', upload_to=upload_to_home, blank=True, null=True)
    link_text = models.CharField('Текст кнопки', max_length=80, default='Смотреть')
    link_url = models.CharField('Ссылка', max_length=220, default='/catalog/')
    is_active = models.BooleanField('Показывать', default=True)
    sort_order = models.PositiveIntegerField('Порядок', default=100)

    class Meta:
        verbose_name = 'Промо-блок главной'
        verbose_name_plural = 'Промо-блоки главной'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image and hasattr(self.image, 'path'):
            optimize_image_path(self.image.path)


class HomeProductSection(models.Model):
    FEATURED = 'featured'
    NEW = 'new'
    BEST_PRICE = 'best_price'
    BESTSELLER = 'bestseller'
    CATEGORY = 'category'
    MANUAL = 'manual'
    SOURCE_CHOICES = [
        (FEATURED, 'Товары с галочкой “Показывать на главной”'),
        (NEW, 'Новинки'),
        (BEST_PRICE, 'Хорошая цена'),
        (BESTSELLER, 'Хиты продаж'),
        (CATEGORY, 'Из выбранной категории'),
        (MANUAL, 'Выбранные вручную ниже'),
    ]

    title = models.CharField('Название секции', max_length=140)
    subtitle = models.CharField('Подзаголовок', max_length=220, blank=True)
    badge = models.CharField('Маленькая надпись', max_length=80, blank=True)
    source = models.CharField('Какие товары показывать', max_length=30, choices=SOURCE_CHOICES, default=FEATURED)
    category = models.ForeignKey(Category, verbose_name='Категория для секции', on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, verbose_name='Товары вручную', blank=True, related_name='home_sections')
    limit = models.PositiveIntegerField('Сколько товаров показать', default=8)
    is_active = models.BooleanField('Показывать секцию', default=True)
    sort_order = models.PositiveIntegerField('Порядок', default=100)

    class Meta:
        verbose_name = 'Секция товаров на главной'
        verbose_name_plural = 'Секции товаров на главной'
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.title

    def get_products(self):
        base = Product.objects.filter(is_active=True).select_related('category')
        if self.source == self.MANUAL:
            return self.products.filter(is_active=True).select_related('category')[: self.limit]
        if self.source == self.NEW:
            return base.filter(is_new=True)[: self.limit]
        if self.source == self.BEST_PRICE:
            return base.filter(is_best_price=True)[: self.limit]
        if self.source == self.BESTSELLER:
            return base.filter(is_bestseller=True)[: self.limit]
        if self.source == self.CATEGORY and self.category:
            return base.filter(category=self.category)[: self.limit]
        return base.filter(is_featured=True)[: self.limit]


class ContactRequest(models.Model):
    PRODUCT_ORDER = 'product_order'
    GENERAL = 'general'
    REQUEST_TYPES = [
        (PRODUCT_ORDER, 'Заявка по товару'),
        (GENERAL, 'Общее сообщение'),
    ]

    request_type = models.CharField('Тип заявки', max_length=30, choices=REQUEST_TYPES, default=GENERAL)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')
    name = models.CharField('Имя', max_length=120)
    phone = models.CharField('Телефон', max_length=80)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Город / адрес', max_length=255, blank=True)
    message = models.TextField('Комментарий', blank=True)
    source_page = models.CharField('Страница-источник', max_length=500, blank=True)
    ip_address = models.GenericIPAddressField('IP-адрес', blank=True, null=True)
    user_agent = models.TextField('User-Agent / устройство', blank=True)
    is_processed = models.BooleanField('Обработано', default=False)
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка клиента'
        verbose_name_plural = 'Заявки клиентов'
        ordering = ['-created_at']

    def __str__(self):
        target = f' — {self.product}' if self.product else ''
        return f'{self.name} {self.phone}{target}'
