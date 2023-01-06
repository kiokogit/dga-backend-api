
from rest_framework import permissions

from shared_utils.utils import GetUser, GetUsersList

class StaffPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = GetUser(
            request=request
        ).get_logged_in_user()
        if user.user_type not in ['INTERNAL STAFF']: # type:ignore
            return False
        return True

class BookingPermission(permissions.BasePermission):
    def has_permission(self, request, view):

        return GetUsersList(
            request=request,
            roles=["BOOKING MANAGER", "BOOKING OFFICER", "GENERAL MANAGER"]
        ).logged_user_has_role()

        
class SMTPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return GetUsersList(
            request=request,
            roles=["FINANCE OFFICER", "GENERAL MANAGER", "CEO", "DIRECTOR"]
        ).logged_user_has_role()