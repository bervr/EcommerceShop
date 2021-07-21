from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from mainapp.models import Product, ProductCategory
from authapp.models import ShopUser
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from adminapp.forms import ShopUserRegisterForm, ShopUserEditForm, ProductCategoryEditForm, ProductCategoryCreateForm, ProductEditForm


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    model = ShopUser
    # exclude = ['password']
    template_name = 'adminapp/edit.html'
    context_object_name = 'user'
    success_url = reverse_lazy('admin_staff:users')
    fields = ('username','first_name', 'last_name') #'__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/new_user.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'создание категории'})
        return context

class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('admin_staff:users')

    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(ShopUser, pk=pk)
        if request.method == 'POST':
            user.is_active = False
            user.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Удаление пользователя'})
        return context



class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_create.html'
    form_class = ProductCategoryCreateForm
    success_url = reverse_lazy('admin_staff:categories')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'создание категории'})
        return context


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    # context_object_name = 'category'
    success_url = reverse_lazy('admin_staff:categories')
    form_class = ProductCategoryEditForm


    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get_initial(self, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     initial = super().get_initial()
    #     # initial = initial.copy()
    #     initial['category'] = ProductCategory.objects.get(pk=pk)
    #     return initial

    def get_context_data(self, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        # context = super().get_context_data(**kwargs)
        context.update({'title': 'изменение категории'})
        return context

    def form_valid(self,form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print('Применяется скидка к товарам')
                self.object.product_set.update(price=F('price')*(1-discount/100))
                # db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    context_object_name = 'category_to_delete'
    success_url = reverse_lazy('admin_staff:categories')

    def post(self, request, pk, *args, **kwargs):
        category = get_object_or_404(ProductCategory, pk=pk)
        if request.method == 'POST':
            category.change_activity()
            return HttpResponseRedirect(reverse('admin_staff:categories'))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Удаление категории'})
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    context_object_name = 'objects'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        category = get_object_or_404(ProductCategory, pk= pk)
        objects = Product.objects.filter(category = category)
        context.update({'title': 'Продукты категории',
                        'category': category,
                        'pk': pk,
                        'objects': objects
                        })
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product.html'
    form_class = ProductEditForm

    def get_initial(self, **kwargs):
        initial = super().get_initial()
        initial = initial.copy()
        pk = self.kwargs.get('pk')
        initial['category'] = ProductCategory.objects.get(pk= pk)
        return initial

    def get_success_url(self, **kwargs):
        pk = self.kwargs.get('pk')
        return reverse('admin_staff:products', args=[pk])

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        category = ProductCategory.objects.get(pk= pk)
        context.update({'title': 'новый продукт',
                        'category': category,
                        'pk': pk,
                        })
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductReadView(DetailView):
    model = Product
    template_name = 'adminapp/product_about.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product.html'
    form_class = ProductEditForm
    # fields = "__all__"

    def get_initial(self, **kwargs):
        pk = self.kwargs.get('pk')
        initial = super().get_initial()
        initial = initial.copy()
        initial['product'] = Product.objects.get(pk=pk)
        return initial

    def get_success_url(self, **kwargs):
        product_pk = self.kwargs.get('pk')
        pk = Product.objects.get(pk=product_pk).category.pk
        return reverse('admin_staff:products', args=[pk])

    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        product = Product.objects.get(pk= pk)
        category = product.category
        context.update({'title': 'редактировать продукт',
                        'product': product,
                        'category': category,
                        })
        return context

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminapp/product_delete.html'
    context_object_name = 'product'

    def get_success_url(self, **kwargs):
        product_pk = self.kwargs.get('pk')
        pk = Product.objects.get(pk=product_pk).category.pk
        return reverse('admin_staff:products', args=[pk])

    def post(self, request, pk, *args, **kwargs):
        if request.method == 'POST':
            product = Product.objects.get(pk=pk)
            category = product.category
            product.is_active = False
            product.state_active = False
            product.save()
            return HttpResponseRedirect(reverse('admin_staff:products', args=[category.pk]))

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

