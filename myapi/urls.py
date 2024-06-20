from django.urls import path, include
from myapi import views
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


router = routers.DefaultRouter()
#router.register(r'users',views.UserView,'users')

schema_view = get_schema_view(
    openapi.Info(
        title="Tu API",
        default_version='v1',
        description="Descripción de tu API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("chatbot_response/",views.chatbot_response, name='chatbot_response'),
    path("mascot_message/",views.mascot_message, name='mascot_message'),
    path('forum', views.ForumView.as_view(), name='forum'),
    path('register', views.user_register, name='register'),
	path('login', views.user_login, name='login'),
	path('logout', views.user_logout, name='logout'),
	path('user', views.user_view, name='user'),
    path('transform', views.transform, name='transform'),
    path('restart_flow', views.restart_flow, name='restart_flow'),
    path('translate', views.translate, name='translate'),
    path('upload_scenary', views.upload_scenary, name='upload_scenary'),
    path('upload_training', views.upload_training, name='upload_training'),
    path('upload_combined', views.upload_combined, name='upload_combined'),
    path('delete_flow', views.delete_flow, name='delete_flow'),
    path('scenarios', views.scenarios, name='scenarios'),
    path('flows/', views.get_flows_by_scenario_url, name='get_flows_by_scenario_url'),
    path('start_flow', views.update_flow_manager, name='start_flow'),
    path('search_student/', views.search_student, name='search_student'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('messages/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('messages/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('scenarios/<str:scenario_name>/flows', views.get_flows_by_scenario, name='get_flows_by_scenario'),
    path('forum/messages', views.forum_messages, name='forum_messages'),
    path('check_chatbot', views.check_chatbot, name='check_chatbot'),
    path('submit_conversation', views.submit_conversation, name='submit_conversation'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]