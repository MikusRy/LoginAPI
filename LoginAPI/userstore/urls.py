from django.urls import path
from LoginAPI.userstore import views

urlpatterns = [
    path('user/', views.user),
    path('user/<token>', views.user),
    path('user/passwd', views.user_passwd),

    path('token/', views.token),
    path('token/refresh', views.token_refresh),
]