from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from adminapp.forms import ShopUserCreationAdminForm, ShopUserUpdateAdminForm, ProductCategoryEditForm, ProductEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class UsersListView(ListView):
    model = ShopUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoriesListView(ListView):
    model = ProductCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'админка/категории'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    success_url = reverse_lazy('myadmin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/создание'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('myadmin:categories')
    form_class = ProductCategoryEditForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('myadmin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductsListView(ListView):
    model = Product
    ordering = ['-is_active', 'name']

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['title'] = 'Список товаров'
        return context

    def get_queryset(self):
        queryset = Product.objects.filter(category=self.kwargs['pk'])
        return queryset


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductEditForm

    def get_context_data(self, **kwargs):
        self.success_url = reverse_lazy('myadmin:products', kwargs={'pk': self.kwargs['pk']})
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'продукты/создание'
        context['category'] = category
        return context

    def get_initial(self):
        self.initial['category'] = self.kwargs['pk']
        return self.initial

    def get_success_url(self):
        return reverse_lazy('myadmin:products', kwargs=self.kwargs)


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

    return render(request, 'mainapp/product_form.html', context)


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/подробнее'
        return context


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        category = get_object_or_404(Product, pk=self.kwargs['pk']).category.pk
        return reverse_lazy('myadmin:products', kwargs={'pk': category})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/удаление'
        return context

    def delete(self, request, *args, **kwargs):
        object = get_object_or_404(Product, pk=kwargs['pk'])
        object.is_active = False
        object.save()
        return HttpResponseRedirect(self.get_success_url())


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