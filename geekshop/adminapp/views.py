from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Products
from adminapp.forms import ShopUserAdminEditForm

from authapp.forms import ShopUserRegisterForm
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from adminapp.forms import ProductEditForm


class AccessMixin:

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))

    else:
        user_form = ShopUserRegisterForm()

    context = {
        'form': user_form,
    }

    return render(request, 'adminapp/user_form.html', context)


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#
#     context = {
#         'object_list': ShopUser.objects.all().order_by('-is_active')
#     }
#
#     return render(request, 'adminapp/users.html', context)

class UserListView(AccessMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('adminapp:user_list'))

    else:
        user_form = ShopUserAdminEditForm(instance=current_user)

    context = {
        'form': user_form,
    }

    return render(request, 'adminapp/user_form.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        if current_user.is_active:
            current_user.is_active = False
        else:
            current_user.is_active = True
        current_user.save()
        return HttpResponseRedirect(reverse('adminapp:user_list'))

    context = {
        'object': current_user,
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):

    context = {

    }

    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):

    context = {
        'object_list': ProductCategory.objects.all().order_by('-is_active')
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request):

    context = {

    }

    return render(request, '', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request):

    context = {

    }

    return render(request, '', context)


# @user_passes_test(lambda u: u.is_superuser)
# def product_create(request):
#
#     context = {
#
#     }
#
#     return render(request, '', context)

class ProductCreateView(AccessMixin, CreateView):
    model = Products
    template_name = 'adminapp/products_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        return reverse('adminapp:product_list', args=[self.kwargs['pk']])


# @user_passes_test(lambda u: u.is_superuser)
# def products(request, pk):
#
#     context = {
#         'category': get_object_or_404(ProductCategory, pk=pk),
#         'object_list': Products.objects.filter(category__pk=pk).order_by('-is_active')
#     }
#
#     return render(request, 'adminapp/products.html', context)

class ProductsListView(AccessMixin, ListView):
    model = Products
    template_name = 'adminapp/products.html'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['category'] = get_object_or_404(ProductCategory, pk=self.kwargs.get('pk'))
        return context_data

    def get_queryset(self):
        return Products.objects.filter(category__pk=self.kwargs.get('pk'))


# @user_passes_test(lambda u: u.is_superuser)
# def product_update(request):
#
#     context = {
#
#     }
#
#     return render(request, '', context)

class ProductUpdateView(AccessMixin, UpdateView):
    model = Products
    template_name = 'adminapp/products_form.html'
    form_class = ProductEditForm

    def get_success_url(self):
        product_item = Products.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])


# @user_passes_test(lambda u: u.is_superuser)
# def product_delete(request):
#
#     context = {
#
#     }
#
#     return render(request, '', context)

class ProductDeleteView(AccessMixin, DeleteView):
    model = Products
    template_name = 'adminapp/products_delete.html'

    def get_success_url(self):
        product_item = Products.objects.get(pk=self.kwargs['pk'])
        return reverse('adminapp:product_list', args=[product_item.category_id])

    # def delete(self, request, *args, **kwargs):
    #     if self.object.is_active:
    #         self.object.is_active = False
    #     else:
    #         self.object.is_active = True
    #     self.object.save()
    #     return HttpResponseRedirect(reverse('adminapp:product_list', args=[self.object.category_id]))


# @user_passes_test(lambda u: u.is_superuser)
# def product_detail(request, pk):
#
#     context = {
#
#     }
#
#     return render(request, '', context)

class ProductDetailView(AccessMixin, DetailView):
    model = Products
    template_name = 'adminapp/product_detail.html'
