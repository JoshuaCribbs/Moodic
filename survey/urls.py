from django.urls import path
from django.conf.urls import url

from recommend import views as recViews
from . import views

#url patterns for use y the various functions of the survey
# index is the base url thats loaded on application start
# increment is used to display the next question to the user
# search is used to return search results
# submit is used to send the survey data to the Reccomender app
# surveyLikeSong used a regex expression to return a given liked song so that it can be stored in the users liked songs
urlpatterns = [
    path('', views.index, name='index'),
    path('/', views.increment, name = 'increment'),
    path('search/', views.songSelect, name = 'songSelect'),
    path('complete/', views.Submit, name = 'submit'),
    # Used for connecting like buttons to appropriate endpoint
    url(r'^connect/(?P<songID>.+)$', views.surveyLikeSong, name='surveyLikeSong'),
]