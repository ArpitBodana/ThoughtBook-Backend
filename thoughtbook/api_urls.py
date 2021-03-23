from django.urls import path,include
from . import views

urlpatterns=[
    path('thoughtbook/generic/',views.ThoughtBookApi.as_view()),
    path('thoughtbook/generic/<int:id>',views.ThoughtBookApi.as_view()),
    path('thoughtbook/generic2/',views.ThoughtBookApi2.as_view()),
    path('thoughtbook/generic2/<int:id>',views.ThoughtBookApi2.as_view()),
   

]