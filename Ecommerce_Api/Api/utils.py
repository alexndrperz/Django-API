import random
import string
from .authentications import IsAdmin, IsSeller, IsChecker, IsBuyer, IsGroupAccepted
from django.utils import timezone
from datetime import datetime, timedelta

class services:
    def generate_invitation_code(length=15):
        """Genera un codigo de invitacion aleatorio."""
        letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for _ in range(length))

    def hasOrNotPermission(clss, request, view,obj=None,authClass=None, oneObj=False):
        userComp={}
        if authClass != None:
            if oneObj== False:
                for item in authClass:
                    userComp[item.__name__] = True if item.has_permission(clss, request, view) else False
            else:
                for item in authClass:
                    userComp[item.__name__] = True if item.has_object_permission(clss, request, view,obj) else False
        return userComp

    def Count_24hours_users(Instance):
        now_str = str(timezone.now())
        
        last24Hours = timedelta(hours=24)
        now = datetime.strptime(now_str, "%Y-%m-%d %H:%M:%S.%f%z")
        print(now)

        las24hoursUsers = Instance.objects.filter(registro__range=(last24Hours, now)) 
        print("test")
        count_users= last24hoursUsers.count()
        return count_users