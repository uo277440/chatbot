from django.urls import path, include
from myapi import views
from rest_framework import routers


router = routers.DefaultRouter()
#router.register(r'users',views.UserView,'users')

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path("chatbot_response/",views.chatbot_response, name='chatbot_response'),
    path("mascot_message/",views.mascot_message, name='mascot_message'),
    path('register', views.UserRegister.as_view(), name='register'),
	path('login', views.UserLogin.as_view(), name='login'),
	path('logout', views.UserLogout.as_view(), name='logout'),
	path('user', views.UserView.as_view(), name='user'),
]