from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactRequestForm
from .models import (
    Category,
    ContactRequest,
    HomeBanner,
    HomeProductSection,
    HomeStat,
    PageContent,
    Product,
    PromoBlock,
)


def get_client_ip(request):
    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def home(request):
    page = PageContent.objects.filter(key=PageContent.HOME).first()
    banners = HomeBanner.objects.filter(is_active=True).order_by('sort_order', 'id')[:5]
    main_banner = banners[0] if banners else None
    promo_blocks = PromoBlock.objects.filter(is_active=True).order_by('sort_order', 'id')[:4]
    stats = HomeStat.objects.filter(is_active=True).order_by('sort_order', 'id')[:4]
    categories = Category.objects.filter(is_active=True, show_on_home=True).order_by('sort_order', 'title')[:8]
    home_sections = (
        HomeProductSection.objects
        .filter(is_active=True)
        .select_related('category')
        .prefetch_related('products', 'products__category')
        .order_by('sort_order', 'id')
    )

    prepared_sections = []
    for section in home_sections:
        products = list(section.get_products())
        if products:
            prepared_sections.append({
                'section': section,
                'products': products,
            })

    featured_products = (
        Product.objects
        .filter(is_active=True, is_featured=True)
        .select_related('category')
        .order_by('home_sort_order', '-created_at')[:8]
    )

    return render(request, 'catalog/home.html', {
        'page': page,
        'main_banner': main_banner,
        'banners': banners,
        'promo_blocks': promo_blocks,
        'stats': stats,
        'featured_products': featured_products,
        'home_sections': prepared_sections,
        'categories': categories,
        'form': ContactRequestForm(),
    })


def about(request):
    page = PageContent.objects.filter(key=PageContent.ABOUT).first()
    return render(request, 'catalog/about.html', {
        'page': page,
        'form': ContactRequestForm(),
    })


def catalog(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True).order_by('sort_order', 'title')

    selected_category = request.GET.get('category', '').strip()
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', '').strip()

    selected_category_obj = None

    if selected_category:
        selected_category_obj = categories.filter(slug=selected_category).first()
        products = products.filter(category__slug=selected_category)

    if query:
        products = products.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(description__icontains=query)
            | Q(sku__icontains=query)
            | Q(colors__icontains=query)
            | Q(sizes__icontains=query)
            | Q(material__icontains=query)
        )

    if sort == 'price_asc':
        products = products.order_by('price', 'title')
    elif sort == 'price_desc':
        products = products.order_by('-price', 'title')
    elif sort == 'new':
        products = products.order_by('-is_new', '-created_at')
    else:
        products = products.order_by('home_sort_order', '-is_featured', '-created_at')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    banners = HomeBanner.objects.filter(is_active=True).order_by('sort_order', 'id')[:5]
    stats = HomeStat.objects.filter(is_active=True).order_by('sort_order', 'id')[:4]

    return render(request, 'catalog/catalog.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'selected_category_obj': selected_category_obj,
        'query': query,
        'sort': sort,
        'banners': banners,
        'stats': stats,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('images'),
        slug=slug,
        is_active=True,
    )

    related_products = (
        Product.objects
        .filter(is_active=True, category=product.category)
        .exclude(pk=product.pk)
        .select_related('category')
        .order_by('home_sort_order', '-created_at')[:4]
    )

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