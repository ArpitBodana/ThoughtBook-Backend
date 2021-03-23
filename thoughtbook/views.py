from django.shortcuts import render
from . serializer import thoughtSerializer,RegisterSerializer,UserSerializer,ChangePasswordSerializer
from rest_framework import generics,mixins, permissions
from . models import thoughts
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from .permissions import IsUser
# Create your views here.
def home(self):
    return HttpResponse("this is home")

class ThoughtBookApi(generics.GenericAPIView,
mixins.CreateModelMixin,
mixins.DestroyModelMixin,
mixins.UpdateModelMixin,
mixins.RetrieveModelMixin,
mixins.ListModelMixin):
    serializer_class = thoughtSerializer
    queryset = thoughts.objects.all()
    lookup_field="id"
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsUser]
    def get(self,request,id=None):
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)
    def post(self,request):
        return self.create(request)
    
    def perform_create(self,serializer):
        return serializer.save(user=self.request.user)
   

class ThoughtBookApi2(generics.GenericAPIView,mixins.UpdateModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,
mixins.ListModelMixin):
    serializer_class = thoughtSerializer
    queryset = thoughts.objects.all()
    lookup_field="id"
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,IsUser]

    
            
    def get(self,request,id=None):
       
        if id:
            return self.retrieve(request,id)
        else:
            return self.list(request)
    def put(self,request,id=None):
        return self.update(request,id)
    def delete(self,request,id=None):
        return self.destroy(request,id)
    def perform_update(self,serializer):
        name=str(self.request.user)
        return serializer.save(user=name)




class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user,context=self.get_serializer_context()).data,
            "token":AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    authentication_classes = []
    permission_classes = (permissions.AllowAny,)
   

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
