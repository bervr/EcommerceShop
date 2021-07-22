from django.conf import settings
from django.test import TestCase, Client
from authapp.models import ShopUser
# Create your tests here.

class UserManagementTestCase(TestCase):
    username = 'django'
    email = 'dj@gb.local'
    password = '123gb456django'
    status_code_success = 200
    status_code_redirect = 302

    new_user_data = {
        'username': 'django1',
        'first_name': 'django1',
        'last_name': 'django1',
        'password1': 'G12eekbrains',
        'password2': 'G12eekbrains',
        'email': 'django1@gb.local',
        'age': '33',

        }


    def setUp(self):
       self.user = ShopUser.objects.create_superuser(username=self.username,email=self.email,password=self.password)
       self.client = Client()


    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

        self.client.login(username=self.username, password =self.password)
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        response = self.client.get('/')
        self.assertContains(response, 'Пользователь', status_code=self.status_code_success)
        self.assertEqual(response.context['user'], self.user)



    class TestUserBasketManagement(TestCase):
        def test_basket_login_redirect(self):
            # без логина должен переадресовать
            response = self.client.get('/basket/')
            self.assertEqual(response.url, '/auth/login/?next=/basket/')
            self.assertEqual(response.status_code, self.status_code_redirect)

            # с логином все должно быть хорошо
            self.client.login(username=self.username, password =self.password)

            response = self.client.get('/basket/')
            self.assertEqual(response.status_code, self.status_code_success)
            self.assertEqual(list(response.context['basket']), [])
            self.assertEqual(response.request['PATH_INFO'], '/basket/')
            self.assertIn('Ваша корзина, Пользователь', response.content.decode())

    def test_user_logout(self):
        # данные пользователя
        self.client.login(username=self.username, password =self.password)

        # логинимся
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertFalse(response.context['user'].is_anonymous)

        # выходим из системы
        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, self.status_code_redirect)

        # главная после выхода
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_register(self):

        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        # логин с данными пользователя

        # логин без данных пользователя
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertEqual(response.context['title'], 'регистрация')
        self.assertTrue(response.context['user'].is_anonymous)

        # логин с данными пользователя
        response = self.client.post('/auth/register/', data=self.new_user_data,)

        self.assertEqual(response.status_code, self.status_code_success)
        # self.assertFalse(response.context['user'].is_anonymous)

        new_user = ShopUser.objects.get(username=self.new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/auth/activate/{new_user.email}/{new_user.activation_key}'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, self.status_code_success)


        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)





