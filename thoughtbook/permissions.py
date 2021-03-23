from rest_framework import permissions
from django.conf import settings


class IsUser(permissions.BasePermission):
   
    def has_permission(self,request,view):
        return True
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        name = str(request.user)
        return name ==obj.user
            

   