import random

from django.shortcuts import render, get_object_or_404
from mainapp.models import Products, ProductCategory

from basketapp.models import Basket


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return None


def get_hot_product():
    return random.sample(list(Products.objects.all()), 1)[0]


def get_same_products(hot_product):
    product_list = Products.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return product_list


def index(request):
    context = {
        'title': 'Главная',
        'products': Products.objects.all(),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context=context)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
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
        context = {
            'links_menu': links_menu,
            'title': 'Продукты',
            'category': category_item,
            'products': product_list,
            'basket': get_basket(request.user)
        }
        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)
    context = {
        'links_menu': links_menu,
        'title': 'Продукты',
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    links_menu = ProductCategory.objects.all()
    context = {
        'product': get_object_or_404(Products, pk=pk),
        'links_menu': links_menu,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/product.html', context=context)

