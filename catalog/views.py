from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactRequestForm
from .models import Category, ContactRequest, PageContent, Product


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def home(request):
    page = PageContent.objects.filter(key=PageContent.HOME).first()
    featured_products = Product.objects.filter(is_active=True, is_featured=True).select_related('category')[:8]
    categories = Category.objects.filter(is_active=True)[:8]
    return render(request, 'catalog/home.html', {
        'page': page,
        'featured_products': featured_products,
        'categories': categories,
        'form': ContactRequestForm(),
    })


def about(request):
    page = PageContent.objects.filter(key=PageContent.ABOUT).first()
    return render(request, 'catalog/about.html', {'page': page, 'form': ContactRequestForm()})


def catalog(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    selected_category = request.GET.get('category', '').strip()
    query = request.GET.get('q', '').strip()

    if selected_category:
        products = products.filter(category__slug=selected_category)
    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
            | Q(sku__icontains=query)
            | Q(colors__icontains=query)
            | Q(sizes__icontains=query)
        )

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/catalog.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'query': query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('category').prefetch_related('images'), slug=slug, is_active=True)
    related_products = Product.objects.filter(is_active=True, category=product.category).exclude(pk=product.pk)[:4]
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'form': ContactRequestForm(),
    })


@require_POST
def create_request(request):
    form = ContactRequestForm(request.POST)
    product_id = request.POST.get('product_id')
    product = None
    if product_id:
        product = Product.objects.filter(pk=product_id, is_active=True).first()

    if form.is_valid():
        contact_request = form.save(commit=False)
        contact_request.product = product
        contact_request.request_type = ContactRequest.PRODUCT_ORDER if product else ContactRequest.GENERAL
        contact_request.source_page = request.META.get('HTTP_REFERER', '')[:500]
        contact_request.ip_address = get_client_ip(request)
        contact_request.user_agent = request.META.get('HTTP_USER_AGENT', '')
        contact_request.save()
        messages.success(request, 'Заявка отправлена. Администратор увидит её в панели управления.')
        return redirect('catalog:contact_success')

    messages.error(request, 'Проверьте имя и телефон. Эти поля обязательны.')
    if product:
        return redirect(product.get_absolute_url())
    return redirect('catalog:home')


def contact_success(request):
    return render(request, 'catalog/contact_success.html')
