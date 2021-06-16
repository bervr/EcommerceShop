from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser

from adminapp.forms import ShopUserRegisterForm,ShopUserEditForm,ProductCategoryEditForm,ProductCategoryCreateForm,ProductEditForm


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/users.html', context=context)

@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'Создать нового пользователя'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'adminapp/new_user.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'редактирование пользователя'
    user = ShopUser.objects.get(pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))
    else:
        edit_form = ShopUserEditForm(instance=user)

    content = {'title': title, 'edit_form': edit_form, 'pk': pk}

    return render(request, 'adminapp/edit.html', content)

@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = ShopUser.objects.get(pk=pk)
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admin_staff:users'))



@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории/создание'
    if request.method == 'POST':
        category_form = ProductCategoryCreateForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryCreateForm()

    context = {'title': title,
               'category_form': category_form,
               }

    return render(request, 'adminapp/category_create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категории/изменение'
    category = ProductCategory.objects.get(pk=pk)

    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES,instance=category)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryEditForm(instance=category)


    context = {'title': title,
               'category_form': category_form,
               'pk':pk
               }

    return render(request, 'adminapp/category_create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category = ProductCategory.objects.get(pk=pk)
    category.delete()
    # category.save()
    return HttpResponseRedirect(reverse('admin_staff:categories'))

@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'новый продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})  # вот понятно что RTFM, но я бы до этого за
        # месяц не додумался

    context = {'title': title,
               'product_form': product_form,
               'category': category,
               'pk': pk
               }
    return render(request, 'adminapp/product.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = ' о продукте'
    product = get_object_or_404(Product, pk=pk)
    content = {'title': title,
               'object': product,
               }

    return render(request, 'adminapp/product_about.html', content)



@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin_staff:product_update', args=[product.pk]))
    else:
        product_form = ProductEditForm(instance=product)
    context = {'title': title,
               'product_form': product_form,
               'product':product
               }

    return render(request, 'adminapp/product.html', context)

@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    category_pk = product.category.pk
    product.is_active = False
    product.save()
    return HttpResponseRedirect(reverse( 'admin_staff:products' , args=[category_pk]))
