from django.urls import path, re_path
import authapp.views as authapp

app_name= 'authapp'

urlpatterns = [

   path('login/', authapp.login, name='login'),
   path('logout/', authapp.logout, name='logout'),
   path('profile/', authapp.edit, name='edit'),
   path('register/', authapp.register, name='register'),
   path('activate/<email>/<key>', authapp.activate, name='activate'),

]
