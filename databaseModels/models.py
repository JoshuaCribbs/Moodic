from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class moods(models.Model):
    moodName = models.CharField(max_length=25)
    
class userSettings(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    
class playlists(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    mood = models.CharField(max_length=25)
    moodID = models.ForeignKey(moods, on_delete=models.CASCADE)
   
class songs(models.Model):
    artist = models.CharField(max_length=1000)
    title = models.CharField(max_length=25)
    genre = models.CharField(max_length=1000)
    acousticness = models.FloatField()
    danceability = models.FloatField()
    energy = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    timeSignature = models.IntegerField()
    valence = models.FloatField()
    duration = models.FloatField()
    songKey = models.IntegerField()
    explicit = models.BooleanField()
    loudness = models.FloatField()
    name = models.CharField(max_length=1000)
    spotifyID = models.CharField(max_length=22)
    popularity = models.IntegerField()
    year = models.CharField(max_length=4)    
    
class playlistSongs(models.Model):
    playlistID = models.ForeignKey(playlists, on_delete=models.CASCADE)
    songID = models.ForeignKey(songs, on_delete=models.CASCADE)

class likedSongs(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    songID = models.ForeignKey(songs, on_delete=models.CASCADE)
    liked = models.BooleanField()
    moodID = models.ForeignKey(moods, on_delete=models.CASCADE)
    
class idealSongs(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    moodID = models.ForeignKey(moods, on_delete=models.CASCADE)
    acousticness = models.FloatField()
    danceability = models.FloatField()
    energy = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    mode = models.IntegerField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    timeSignature = models.IntegerField()
    valence = models.FloatField()
    duration = models.FloatField()
    songKey = models.IntegerField()
    explicit = models.BooleanField()
    loudness = models.FloatField()
    popularity = models.IntegerField()
    year = models.CharField(max_length=4)
    
class surveyData(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    moodID = models.ForeignKey(moods, on_delete=models.CASCADE)
    acousticness = models.FloatField()
    danceability = models.FloatField()
    energy = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    valence = models.FloatField()
    loudness = models.FloatField()
    year = models.CharField(max_length=4)