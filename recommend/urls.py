from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('survey/', include('survey.urls')),
    path('newPlaylist/', views.newplaylist, name='newplaylist'),
    path('likedSongs/', views.likedsongs, name='likedsongs'),
    path('accountSettings/', views.accountsettings, name='accountsettings'),
    path('surveyPage/', views.surveypage, name='surveypage'),
    # Used for connecting like/dislike buttons to appropriate endpoint
    url(r'^connect/(?P<songID>.+)/(?P<like>.+)$', views.recommendLikeSong, name='recommendLikeSong'),

    # Set path for Django's build in change password view
    # Used when selecting change password from account settings
    path('change_password/',
         auth_views.PasswordChangeView.as_view(
             template_name="recommend/ChangePassword.html",
             success_url='/'
         ),
         name='change_password'),
]