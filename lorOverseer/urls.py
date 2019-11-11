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
from stats.views import StatsListView, StatsDetailView, StatsCreateView, StatsUpdateView, StatsDeleteView, UserGameListView

urlpatterns = [
    path('', stat_views.Home, name='stats'),
    path('stats/games/', StatsListView.as_view(), name='games'),
    path('stats/games/<int:pk>/', StatsDetailView.as_view(), name='gameDetails'),
    path('stats/games/create/', StatsCreateView.as_view(), name='gameCreate'),
    path('stats/games/<int:pk>/update/', StatsUpdateView.as_view(), name='gameUpdate'),
    path('stats/games/<int:pk>/delete/', StatsDeleteView.as_view(), name='gameDelete'),
    path('about/', stat_views.About, name='about'),
    path('register/', user_views.Register, name='register'),
    path('profile/', user_views.Profile, name='profile'),
    path('profile/games/', UserGameListView.as_view(), name='profileGames'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('passwordReset/', auth_views.PasswordResetView.as_view(template_name='users/passwordReset.html'), name='passwordReset'),
    path('passwordReset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/passwordResetDone.html'), name='password_reset_done'),
    path('passwordReset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/passwordResetConfirm.html'), name='password_reset_confirm'),
    path('passwordReset/complete', auth_views.PasswordResetCompleteView.as_view(template_name='users/passwordResetComplete.html'), name='password_reset_complete'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
