from django.contrib.auth.backends import BaseBackend
from datetime import timezone, datetime
import pytz
from .models import User
from django.conf import settings
from django.contrib.auth.backends import ModelBackend

current_timezone = pytz.timezone(settings.TIME_ZONE)

class CustomBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None, *args, **kwargss):
        print('asdasd')
        UserModel = User
        try:
            user = UserModel.objects.get(email=email)
            print(user)
            if user.check_password:
                current_time = datetime.now(current_timezone)
                user.last_login = current_time
                user.save()
                return user
        except UserModel.DoesNotExist:
            return None




class CustomAuthBackend(ModelBackend):

    def check_password(self, password, encoded):
        return super().check_password(password, encoded)

