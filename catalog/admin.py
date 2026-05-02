from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline

from .models import Category, ContactRequest, PageContent, Product, ProductImage, SiteSettings


class ImagePreviewMixin:
    @admin.display(description='Фото')
    def image_preview(self, obj):
        image = getattr(obj, 'image', None) or getattr(obj, 'main_image', None) or getattr(obj, 'hero_image', None) or getattr(obj, 'logo', None)
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
class PageContentAdmin(ModelAdmin):
    list_display = ['key', 'title', 'phone', 'email', 'updated_at']
    search_fields = ['title', 'subtitle', 'body', 'phone', 'email', 'address']
    fieldsets = (
        ('Страница', {'fields': ('key', 'title', 'subtitle', 'body')}),
        ('Изображения', {'fields': ('hero_image', 'second_image')}),
        ('Контакты на странице', {'fields': ('phone', 'email', 'address')}),
    )


@admin.register(Category)
class CategoryAdmin(ImagePreviewMixin, ModelAdmin):
    list_display = ['title', 'slug', 'sort_order', 'is_active', 'image_preview']
    list_editable = ['sort_order', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']


class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt', 'sort_order']


@admin.register(Product)
class ProductAdmin(ImagePreviewMixin, ModelAdmin):
    list_display = ['title', 'category', 'sku', 'price', 'currency', 'is_active', 'is_featured', 'image_preview', 'updated_at']
    list_filter = ['is_active', 'is_featured', 'category', 'created_at']
    list_editable = ['is_active', 'is_featured']
    search_fields = ['title', 'sku', 'short_description', 'description', 'sizes', 'colors', 'material']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['qr_preview', 'created_at', 'updated_at']
    inlines = [ProductImageInline]
    fieldsets = (
        ('Основное', {'fields': ('title', 'slug', 'sku', 'category', 'is_active', 'is_featured')}),
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
