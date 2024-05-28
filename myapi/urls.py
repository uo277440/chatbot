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
    path('transform', views.transform, name='transform'),
    path('restart_flow', views.restart_flow, name='restart_flow'),
    path('translate', views.translate, name='translate'),
    path('upload_scenary', views.upload_scenary, name='upload_scenary'),
    path('upload_training', views.upload_training, name='upload_training'),
    path('upload_combined', views.upload_combined, name='upload_combined'),
    path('scenarios', views.scenarios, name='scenarios'),
    path('flows/', views.get_flows_by_scenario, name='get_flows_by_scenario'),
    path('start_flow', views.update_flow_manager, name='start_flow'),
    path('search_student/', views.search_student, name='search_student'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('messages/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('forum/messages', views.forum_messages, name='forum-messages'),
    
]