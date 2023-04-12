import datetime
import random
from django.conf import settings
from .models import DepartmentModel, RolesModel, UserModel
import boto3            

def get_user_roles(user):
    user_roles = user.roles.filter(
        is_active=True,
        is_deleted=False
    )
    if user_roles.exists():
        return [role for role in user_roles.all()] 
    else:
        return []


class CreateUserRoles:

    def __init__(self, user:object, role, actor:str, department_id):
        self.user = user
        self.role = role
        self.actor_id = actor
        self.department_id = department_id
        self.actor = UserModel.objects.get(id=actor)

    def actor_has_permission(self):
        # if settings.DEBUG:
        #     return True
        # must be department head
        department = DepartmentModel.objects.get(id=self.department_id)
        if not self.actor.roles.filter(
            department=department,
            is_department_head=True
        ).exists():
            return False
        
        # department head can only be added by the executive branch
        if self.role in RolesModel.objects.filter(department__name='EXECUTIVE').all() and not len([role for role in get_user_roles(self.actor) if role.role=="GENERAL MANAGER"]) > 0: #type:ignore
            return False

        else:
            return True


    def add_user_role(self):
        if not self.role:
            return False, f'{self.role.role} is not defined in the system. Contact customer care for assistance'

        __roles = self.user.roles.filter(    # type: ignore
            id=self.role.id
        )   
        __role = __roles.first()
        if __role:
            if __role.is_active:
                pass
            else:
                __role.is_active=True
                __role.is_deleted=False
                __role.date_deleted=None
                __role.save()
            return True, "Role updated successfully"
        else:
            try:
                self.user.roles.add(self.role) # type: ignore
            except Exception as e:
                print(e)
                return False, "role not added"


        return True, "role added successfully to user"

    def remove_user_role(self):
        if not self.actor_has_permission():
            return False, "you do not have permission to remove the role"
        
        role = RolesModel.objects.filter(
            user=self.user,
            role=self.role,
            is_active=True
        ).first()
        if not role:
            return False, "user does not have that role"
        else:
            role.is_active = False,  # type: ignore
            role.is_deleted=True,  # type: ignore
            role.date_deleted = datetime.datetime.now()

            role.save()
        return True, "user role removed successfully"
        

def add_user_role(user, role):
    
    __roles = RolesModel.objects.filter(  
        user=user,
        role=role
    )
    __role = __roles.first()
    if __role:
        if __role.is_active:
            return True
        else:
            __role.is_active=True
            __role.is_deleted=False
            __role.date_deleted=None
            __role.save()
        return True

    RolesModel.objects.create(
        user=user,
        role=role,
        is_active=True
    )

    return True


def validate_email(email:str):

    if not (email.__contains__('@') 
            and len(email) < 254 
            and len(email) > 15 
            and email.split('@')[1].__contains__('.')
            ):
        return False
    return True


def validate_password(passw:str):

    if len(passw) < 8:
        return False
    
    return True


def generate_random_password():

    characters ='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890qwertyuiopasdgfhjklzxcvbnm'

    charactersLength = len(characters)
    result = ''
    for i in range(0, 8):
        result += characters[round(random.random()*(charactersLength-1))]
    
    return result       #type:ignore

def sendemail(subject, message, recipients, headers):
    # django-email-server.py

     # send email for password
    

    return True


def send_staff_account_signup(to_email, password):
    client = boto3.client("ses", region_name="eu-north-1", aws_access_key_id=settings.AWS_ACCESS_ID,
         aws_secret_access_key= settings.AWS_ACCESS_KEY)

    client.send_email(
    Destination={
        'ToAddresses': [
            to_email,
        ],
    },
    Message={
        'Body': {
            'Html': {
                'Charset': 'UTF-8',
                'Data': f'<h3>An access to DGA Staff Portal has been created for you.</h3> <p>Welcome to DGA Staff Portal.</p><h4>Username: {to_email}</h4><h4>Password: {password}</h4> <div>Consider Changing it after login to your preference</div> <div>Feel free to contact DGA Technical team for any support <a href="http://dga-tours.com/public/contact_us" target="_blank">through Here</a>.</div>',
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': 'Welcome to DGA Staff Team',
        },
    },
    Source='dgatours.travel@gmail.com',
    )

    return True
