from django.urls import path, include
from myapi import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users',views.UserView,'users')

urlpatterns = [
    path('hello-world/', views.hello_world, name='hello_world'),
    path("crud/",include(router.urls))
]