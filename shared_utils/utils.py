import datetime
import random
from django.conf import settings
import jwt

from authapp.models import RolesModel, UserModel


def return_headers(request):
        headers = {
            "JWTAUTH":request.headers['JWTAUTH'].split(' ')[1],
            # "Authorization":request.headers["Authorization"].split(' ')[1]
        }
        return headers
    
def get_serializer_context(request):
    headers = return_headers(request)
    # decode jwt
    payload = jwt.decode(headers['JWTAUTH'],key=settings.SECRET_KEY, algorithms=['HS256'])
    
    context = {
        "user_id": payload['user_id'],
        "user_type": payload['user_type'],
        "headers":headers
    }
    return context

class GetUser:
    def __init__(self, request=None, headers=None, id=None) -> None:
        self.request = request
        self.headers = headers
        self.id = id
    
    def get_logged_in_user(self):
        self.id = get_serializer_context(self.request)['user_id']
        # get user by ID
        return self.get_user_by_id()
    
    def get_user_by_id(self):
        try:
            user = UserModel.objects.get(id=self.id)
        except UserModel.DoesNotExist:
            return None
        return user

    def get_user_basic_details(self):
        user = self.get_user_by_id()
        # serialize
        # return serialized data

    def get_user_roles(self):
        user_roles = self.get_user_by_id().roles.objects.all() # type:ignore
        return [role.role for role in user_roles]


class GetUsersList:

    def __init__(self, request=None, roles:list = []) -> None:
        self.request = request
        self.roles = roles

    def get_users_with_role(self):
        users = RolesModel.objects.filter(role__in=self.roles, is_active=True).all()
        if users.exists():
            return users.values("user")
        else:
            return []
    
    def logged_user_has_role(self):
        user_id = GetUser(
            request=self.request
        ).get_logged_in_user().id # type:ignore
        if user_id not in self.get_users_with_role():
            return False
        else:
            return True

def generate_package_ref():
    characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    result = 'PCKG23/'
    charactersLength = len(characters)
    for i in range(0, 10):
        result += characters[round(random.random()*charactersLength)]

    return result

def generate_process_ref(process_code:str):
    return process_code + "23"+ "/" + str(random.randint(0, 2000))
