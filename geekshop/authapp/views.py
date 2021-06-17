from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import  auth
from django.shortcuts import HttpResponseRedirect
from .forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from django.urls import reverse

# Create your views here.
from .models import ShopUser


def login(request):
    title = 'Вход'

    login_form = ShopUserLoginForm(data=request.POST)
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    context = {'title':title, 'login_form': login_form, 'next': next,}
    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    title = 'редактирование'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {'title': title, 'edit_form': edit_form}

    return render(request, 'authapp/edit.html', content)


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            send_activation_link(user)
            return render(request, 'authapp/sended.html')
            # return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    content = {'title': title, 'register_form': register_form}

    return render(request, 'authapp/register.html', content)

def send_activation_link(user):
    activation_link = reverse('authapp:activate', args =[user.email,user.activation_key])
    subject = 'Email confirmation'
    message = f'Open this link for confirm your email {settings.DOMAIN_NAME}{activation_link}'
    email=  send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
    return email


def activate(request, email, key):
    user = ShopUser.objects.filter(email = email).first()
    if user and user.activation_key == key and not user.is_activation_key_expired():
        user.is_active = True
        user.activation_key = ''
        user.is_activation_key_expired = None
        user.save()
        auth.login(request, user)
        # return HttpResponseRedirect(reverse('auth:login'))
    return render(request, 'authapp/activate.html')





