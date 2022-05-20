from django.urls import path
from LoginAPI.userstore import views

urlpatterns = [
    path('user', views.user),
    path('user/activate', views.user_activate),
    path('user/passwd', views.user_passwd),
    path('user/delete', views.user_delete),

    path('token', views.token),
    path('token/refresh', views.token_refresh),
]