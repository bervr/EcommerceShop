
from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests


from authapp.models import ShopUserProfile
from django.conf.global_settings import MEDIA_URL
from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    # print(backend)
    if backend.name != 'vk-oauth2':
        print('wrong backend')
        return
    api_url =f"https://api.vk.com/method/users.get?fields=bdate,sex,about,photo_100&access_token={response['access_token']}&v=5.131"
    vk_response = requests.get(api_url)
    if vk_response.status_code != 200:
        return
    vk_data= vk_response.json()['response'][0]
    if vk_data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if vk_data['sex'] == 2 else ShopUserProfile.FEMALE

    if vk_data['about']:
        user.shopuserprofile.about_me = vk_data['about']

    if vk_data['bdate']:
        bdate = datetime.strptime(vk_data['bdate'], '%d.%m.%Y').date()
        age = relativedelta(datetime.now().date(), bdate).years
        if age < 18:
        # if age < 180:
            user.is_active = False
            raise AuthForbidden ('social_core.backends.vk.VKOAuth2')
        else:
            user.age = age

    if vk_data['photo_100']:
        path =f'/user_avatar/{user.id}.jpg'
        url_photo = vk_data['photo_100']
        user.user_pic = url_photo
        r = requests.get(url_photo)

        if r.status_code == 200:
            with open('media'+path, 'wb') as f:  #костыль
                f.write(r.content)
            user.user_pic = path

    user.save()





