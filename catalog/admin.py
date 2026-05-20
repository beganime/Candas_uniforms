from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    Category,
    ContactRequest,
    HomeBanner,
    HomeProductSection,
    HomeStat,
    PageContent,
    Product,
    ProductImage,
    PromoBlock,
    SiteSettings,
)


class ImagePreviewMixin:
    @admin.display(description='Фото')
    def image_preview(self, obj):
        image = (
            getattr(obj, 'image', None)
            or getattr(obj, 'main_image', None)
            or getattr(obj, 'hero_image', None)
            or getattr(obj, 'logo', None)
        )
        if image:
            return format_html('<img src="{}" style="width:70px;height:70px;object-fit:cover;border-radius:14px;" />', image.url)
        return '—'


@admin.register(SiteSettings)
class SiteSettingsAdmin(ImagePreviewMixin, ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'domain', 'image_preview', 'updated_at']
    fieldsets = (
        ('Основное', {'fields': ('site_name', 'logo', 'hero_badge', 'domain')}),
        ('Контакты', {'fields': ('phone', 'second_phone', 'whatsapp', 'email', 'address', 'instagram', 'telegram')}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(PageContent)
class PageContentAdmin(ImagePreviewMixin, ModelAdmin):
    list_display = ['key', 'title', 'phone', 'email', 'image_preview', 'updated_at']
    search_fields = ['title', 'subtitle', 'body', 'phone', 'email', 'address']
    fieldsets = (
        ('Страница', {'fields': ('key', 'title', 'subtitle', 'body')}),
        ('Изображения', {'fields': ('hero_image', 'second_image')}),
        ('Контакты на странице', {'fields': ('phone', 'email', 'address')}),
    )


@admin.register(HomeBanner)
class HomeBannerAdmin(ImagePreviewMixin, ModelAdmin):
    list_display = ['title', 'badge', 'button_text', 'is_active', 'sort_order', 'image_preview', 'updated_at']
    list_editable = ['is_active', 'sort_order']
    search_fields = ['title', 'subtitle', 'badge', 'button_text']
    fieldsets = (
        ('Текст баннера', {'fields': ('badge', 'title', 'subtitle')}),
        ('Картинка', {'fields': ('image',)}),
        ('Кнопки', {'fields': ('button_text', 'button_url', 'second_button_text', 'second_button_url')}),
        ('Показ', {'fields': ('is_active', 'sort_order')}),
    )


@admin.register(PromoBlock)
class PromoBlockAdmin(ImagePreviewMixin, ModelAdmin):
    list_display = ['title', 'accent_text', 'link_text', 'is_active', 'sort_order', 'image_preview']
    list_editable = ['is_active', 'sort_order']
    search_fields = ['title', 'subtitle', 'accent_text']
    fieldsets = (
        ('Текст', {'fields': ('accent_text', 'title', 'subtitle')}),
        ('Фото и ссылка', {'fields': ('image', 'link_text', 'link_url')}),
        ('Показ', {'fields': ('is_active', 'sort_order')}),
    )


@admin.register(HomeStat)
class HomeStatAdmin(ModelAdmin):
    list_display = ['value', 'label', 'is_active', 'sort_order']
    list_editable = ['is_active', 'sort_order']
    search_fields = ['value', 'label']


@admin.register(Category)
class CategoryAdmin(ImagePreviewMixin, ModelAdmin):
    list_display = ['title', 'slug', 'sort_order', 'is_active', 'show_on_home', 'image_preview']
    list_editable = ['sort_order', 'is_active', 'show_on_home']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt', 'sort_order']


@admin.register(HomeProductSection)
class HomeProductSectionAdmin(ModelAdmin):
    list_display = ['title', 'source', 'category', 'limit', 'is_active', 'sort_order']
    list_editable = ['is_active', 'sort_order', 'limit']
    list_filter = ['source', 'is_active', 'category']
    search_fields = ['title', 'subtitle', 'badge']
    filter_horizontal = ['products']
    fieldsets = (
        ('Заголовок секции', {'fields': ('badge', 'title', 'subtitle')}),
        ('Товары', {'fields': ('source', 'category', 'products', 'limit')}),
        ('Показ', {'fields': ('is_active', 'sort_order')}),
    )


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, ModelAdmin):
    list_display = [
        'title',
        'category',
        'sku',
        'price',
        'old_price',
        'currency',
        'is_active',
        'is_featured',
        'is_new',
        'is_best_price',
        'is_bestseller',
        'home_sort_order',
        'image_preview',
        'updated_at',
    ]
    list_filter = ['is_active', 'is_featured', 'is_new', 'is_best_price', 'is_bestseller', 'category', 'created_at']
    list_editable = ['is_active', 'is_featured', 'is_new', 'is_best_price', 'is_bestseller', 'home_sort_order']
    search_fields = ['title', 'sku', 'short_description', 'description', 'sizes', 'colors', 'material', 'badge_text']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['qr_preview', 'created_at', 'updated_at']
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'sku', 'category', 'is_active')}),
        ('Показ на сайте', {'fields': ('is_featured', 'home_sort_order', 'is_new', 'is_best_price', 'is_bestseller', 'badge_text')}),
        ('Описание', {'fields': ('short_description', 'description')}),
        ('Цена', {'fields': ('price', 'old_price', 'currency')}),
        ('Характеристики', {'fields': ('sizes', 'colors', 'material', 'care')}),
        ('Фото и QR', {'fields': ('main_image', 'qr_preview')}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )

    @admin.display(description='QR-код товара')
    def qr_preview(self, obj):
        if obj and obj.qr_code:
            return format_html('<img src="{}" style="width:130px;height:130px;object-fit:contain;" />', obj.qr_code.url)
        return 'QR-код появится после сохранения товара.'


@admin.register(ContactRequest)
class ContactRequestAdmin(ModelAdmin):
    list_display = ['created_at', 'name', 'phone', 'email', 'product', 'request_type', 'ip_address', 'is_processed']
    list_filter = ['request_type', 'is_processed', 'created_at']
    search_fields = ['name', 'phone', 'email', 'address', 'message', 'ip_address', 'user_agent', 'product__title']
    readonly_fields = ['request_type', 'product', 'name', 'phone', 'email', 'address', 'message', 'source_page', 'ip_address', 'user_agent', 'created_at']
    fieldsets = (
        ('Заявка', {'fields': ('request_type', 'product', 'name', 'phone', 'email', 'address', 'message', 'is_processed')}),
        ('Откуда пришла заявка', {'fields': ('source_page', 'ip_address', 'user_agent', 'created_at')}),
    )

    def has_add_permission(self, request):
        return False
