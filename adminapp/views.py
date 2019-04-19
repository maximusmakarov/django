from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import ShopUserCreationAdminForm, ShopUserUpdateAdminForm, ProductCategoryEditForm, ProductEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': 'админка/пользователи',
        'objects': users_list
    }

    return render(request, 'adminapp/index.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories(request):

    object_list = ProductCategory.objects.all().order_by('-is_active', 'name')

    content = {
        'title': 'админка/категории',
        'object_list': object_list
    }

    return render(request, 'adminapp/productcategory_list.html', content)


@user_passes_test(lambda x: x.is_superuser)
def products(request, pk):

    category = get_object_or_404(ProductCategory, pk=pk)
    object_list = category.product_set.all().order_by('name')

    context = {
        'title': 'админка/продукт',
        'category': category,
        'object_list': object_list,
    }

    return render(request, 'adminapp/product_list.html', context)


@user_passes_test(lambda x: x.is_superuser)
def shopuser_create(request):

    if request.method == 'POST':
        form = ShopUserCreationAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserCreationAdminForm()

    context = {
        'title': 'пользователи/создание',
        'form': form
    }

    return render(request, 'adminapp/shopuser_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def shopuser_update(request, pk):
    current_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = ShopUserUpdateAdminForm(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:index'))
    else:
        form = ShopUserUpdateAdminForm(instance=current_user)

    context = {
        'title': 'пользователи/редактирование',
        'form': form
    }

    return render(request, 'adminapp/shopuser_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def shopuser_delete(request, pk):
    object = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        object.is_active = False
        object.save()
        return HttpResponseRedirect(reverse('myadmin:index'))

    context = {
        'title': 'пользователи/удаление',
        'user_to_delete': object
    }

    return render(request, 'adminapp/shopuser_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def productcategory_create(request):
    if request.method == 'POST':
        form = ProductCategoryEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:categories'))
    else:
        form = ProductCategoryEditForm()

    context = {
        'title': 'категории/создание',
        'form': form
    }

    return render(request, 'adminapp/productcategory_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def productcategory_update(request, pk):
    current_object = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = ProductCategoryEditForm(request.POST, request.FILES, instance=current_object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:categories'))
    else:
        form = ProductCategoryEditForm(instance=current_object)

    context = {
        'title': 'категории/редактирование',
        'form': form
    }

    return render(request, 'adminapp/productcategory_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def productcategory_delete(request, pk):
    object = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        object.is_active = False
        object.save()
        return HttpResponseRedirect(reverse('myadmin:categories'))

    context = {
        'title': 'категории/удаление',
        'object': object
    }

    return render(request, 'adminapp/productcategory_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_create(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:products', kwargs={'pk': pk}))
    else:
        form = ProductEditForm(initial={'category': category})

    context = {
        'title': 'продукты/создание',
        'form': form,
        'category': category
    }

    return render(request, 'adminapp/product_update.html', context)


def product_read(request, pk):
    context = {
        'title': 'продукт/подробнее',
        'object': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'adminapp/product_read.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_update(request, pk):
    product_object = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product_object)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('myadmin:products', kwargs={'pk': product_object.category.pk}))
    else:
        form = ProductEditForm(instance=product_object)

    context = {
        'title': 'продукты/редактирование',
        'form': form,
        'category': product_object.category
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def product_delete(request, pk):
    object = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        object.is_active = False
        object.save()
        return HttpResponseRedirect(reverse('myadmin:products', kwargs={'pk': object.category.pk}))

    context = {
        'title': 'продукты/удаление',
        'object': object,
        'category': object.category

    }

    return render(request, 'adminapp/product_delete.html', context)

