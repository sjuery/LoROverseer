"""lorOverseer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('stats/', include('stats.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from stats import views as stat_views
from stats.views import StatsDetailView, UserGameListView

urlpatterns = [
    path('', stat_views.Overall, name='stats'),
    path('stats/', stat_views.Overall, name='overallStats'),
    path('stats/normal', stat_views.Normal, name='normalStats'),
    path('stats/expeditions', stat_views.Expedition, name='expeditionStats'),
    path('stats/games/', UserGameListView.as_view(), name='games'),
    path('stats/game/<int:pk>/', StatsDetailView.as_view(), name='gameDetails'),
    path('stats/game/', stat_views.Replay, name='gameDetails'),
    path('about/', stat_views.About, name='about'),
    path('profile/', UserGameListView.as_view(), name='profile'),
    #Account Management
    path('register/', user_views.Register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('admin/', admin.site.urls),
    #Password Management
    path('passwordReset/', auth_views.PasswordResetView.as_view(template_name='users/passwordReset.html'), name='passwordReset'),
    path('passwordReset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/passwordResetDone.html'), name='password_reset_done'),
    path('passwordReset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/passwordResetConfirm.html'), name='password_reset_confirm'),
    path('passwordReset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/passwordResetComplete.html'), name='password_reset_complete'),
    path('addGame/', stat_views.AddData, name='addGame'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
