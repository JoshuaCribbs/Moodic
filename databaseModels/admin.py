from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.userSettings)
admin.site.register(models.playlists)
admin.site.register(models.songs)
admin.site.register(models.playlistSongs)
admin.site.register(models.likedSongs)
admin.site.register(models.idealSongs)
admin.site.register(models.moods)
admin.site.register(models.surveyData)