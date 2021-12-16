import random

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from mainapp.models import Products, ProductCategory
from django.conf import settings
from django.core.cache import cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'categories'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category_item = cache.get(key)
        if category_item is None:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category_item)
        return category_item
    return get_object_or_404(ProductCategory, pk=pk)


def get_hot_product():
    return random.sample(list(Products.objects.all()), 1)[0]


def get_same_products(hot_product):
    product_list = Products.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).select_related()[:3]
    return product_list


def index(request):
    context = {
        'title': 'Главная',
        'products': Products.objects.all(),
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None, page=1):
    links_menu = get_links_menu
    if pk is not None:
        if pk == 0:
            product_list = Products.objects.all()
            category_item = {
                'name': 'все',
                'pk': 0
            }
        else:
            category_item = get_object_or_404(ProductCategory, pk=pk)
            product_list = Products.objects.filter(category__pk=pk)

        paginator = Paginator(product_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'category': category_item,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'links_menu': links_menu,
        'title': 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products,
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    links_menu = get_links_menu
    context = {
        'product': get_object_or_404(Products, pk=pk),
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/product.html', context=context)

