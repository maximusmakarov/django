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

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo')),
                                                access_token=response['access_token'],
                                                v='5.95')),
                          None
                          ))

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

    if data['photo']:
        user.avatar = data['photo']
        # temp_image = StringIO()
        # ImageFile.Parser().close().save(temp_image, 'png')
        # temp_image.seek(0)
        # user.avatar = File(temp_image, 'photo')

    user.save()
