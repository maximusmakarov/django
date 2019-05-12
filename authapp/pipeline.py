from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from io import StringIO
from authapp.models import ShopUserProfile
from django.core.files import File
from PIL import Image, ImageFile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https', 'api.vk.com', '/method/users.get', None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200', 'screen_name',
                                                                 'language')),
                                                access_token=response['access_token'], v='5.95')), None))

    resp = requests.get(api_url)

    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        user.age = timezone.now().date().year - bdate.year
        if user.age <= 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['photo_200']:
        user.shopuserprofile.photo_vk = data['photo_200']

    if data['screen_name']:
        user.shopuserprofile.link_social = 'https://vk.com/' + data['screen_name']

    if data['language']:
        if data['language'] == 0:
            user.shopuserprofile.lang = ShopUserProfile.RU
        # elif data['lang'] == 1:
        #     user.shopuserprofile.lang = ShopUserProfile.UK
        # elif data['lang'] == 2:
        #     user.shopuserprofile.lang = ShopUserProfile.BE
        elif data['language'] == 3:
            user.shopuserprofile.lang = ShopUserProfile.EN
        # elif data['lang'] == 4:
        #     user.shopuserprofile.lang = ShopUserProfile.ES
        # elif data['lang'] == 5:
        #     user.shopuserprofile.lang = ShopUserProfile.FI
        # elif data['lang'] == 6:
        #     user.shopuserprofile.lang = ShopUserProfile.DE
        # elif data['lang'] == 7:
        #     user.shopuserprofile.lang = ShopUserProfile.IT
        else:
            user.shopuserprofile.lang = ShopUserProfile.RU
    user.save()
