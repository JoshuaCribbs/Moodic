from django.shortcuts import render, redirect
from django.http import HttpResponse
from databaseModels import models
from scipy.spatial.distance import cdist
import numpy
import heapq


def home(request):
    return render(request, 'recommend/Home-WelcomeScreen.html')
    # When index is activated home.html is rendered.


def newplaylist(request):
    #If a playlist has been created, get playlist from session
    playlist = request.session.get('playlist', [])
    #If a playlist has not been created, create one
    if not playlist:
        #Retrieve relevant information from request/session
        current_user = request.user
        selected_mood = models.moods.objects.get(id=request.session['moodID'])
        genre = request.session['genre']
        year = request.session['year']
        acousticness = request.session['acousticness']
        danceability = request.session['danceability']
        energy = request.session['energy']
        instrumentalness = request.session['instrumentalness']
        liveness = request.session['liveness']
        speechiness = request.session['speechiness']
        tempo = request.session['tempo']
        valence = request.session['valence']
        loudness = request.session['loudness']

        #Send user info and survey answers to playlist generation function
        playlist = generatePlaylist(current_user, selected_mood, genre, year, acousticness, danceability,
                                    energy, instrumentalness, liveness, speechiness, tempo, valence, loudness)
        #Save created playlist to session to prevent loss on page reloading
        request.session['playlist'] = playlist
    return render(request, 'recommend/NewPlaylistPage.html', {'playlist': playlist})


def accountsettings(request):
    return render(request, 'recommend/AccountSettings.html')


def likedsongs(request):
    #Reset results/flag
    showSongs = False
    idList = []
    #Get liked song for current user
    current_user = request.user
    liked = models.likedSongs.objects.filter(userID=current_user)
    #If liked songs exist, process each spotifyID
    if liked.exists():
        for like in liked:
            song = models.songs.objects.get(id=like.songID_id)
            idList.append(song.spotifyID)
        #Flag html that there are songs to display
        showSongs = True
    context = {'idList': idList,
                'showSongs': showSongs,}
    return render(request, 'recommend/LikedSongs.html', context)

    #this is new


def surveypage(request):
    return render(request, 'recommend/SurveyPage.html')


"""The following are functions for the recommender system"""


def generatePlaylist(current_user, selected_mood, genre, decade, acousticness, danceability,
                     energy, instrumentalness, liveness, speechiness, tempo, valence, loudness):
    #Get the user's long term ideal song (based on average of liked songs)
    raw_ideal = get_user_ideal(current_user, selected_mood)
    #Adjust values for current mood according to survey answers
    raw_ideal = adjust_ideal(raw_ideal, acousticness, danceability,
                             energy, instrumentalness, liveness, speechiness, tempo, valence, loudness)
    #Feature engineering
    ideal_song = featurize([raw_ideal])[0]
    #Get filtered candidates for recommendation
    songs = get_subset(decade, genre, current_user, selected_mood)
    #Get top recommendations from candidates
    newPlaylist = recommend(ideal_song, songs)
    return newPlaylist


def adjust_ideal(ideal_song, acousticness, danceability,
                 energy, instrumentalness, liveness, speechiness, tempo, valence, loudness):
    #Adjust all values based on survey answers
    ideal_song.acousticness = adjust_value(
        ideal_song.acousticness, acousticness)
    ideal_song.danceability = adjust_value(
        ideal_song.danceability, danceability)
    ideal_song.energy = adjust_value(ideal_song.energy, energy)
    ideal_song.instrumentalness = adjust_value(
        ideal_song.instrumentalness, instrumentalness)
    ideal_song.liveness = adjust_value(ideal_song.liveness, liveness)
    ideal_song.speechiness = adjust_value(ideal_song.speechiness, speechiness)
    ideal_song.tempo = adjust_value(ideal_song.tempo, tempo)
    ideal_song.valence = adjust_value(ideal_song.valence, valence)
    ideal_song.loudness = adjust_value(ideal_song.loudness, loudness)
    return ideal_song


def adjust_value(ideal_value, survey_value):
    """
    Adjusts long term ideal towards current ideal
    (based on survey answers) by 10% of the
    difference between each value.
    """
    difference = (ideal_value - survey_value) * 0.1
    adjusted_value = ideal_value - difference
    return adjusted_value


def get_user_ideal(current_userID, selected_mood):
    # Gets current user's long term ideal song features
    user_ideal = models.idealSongs.objects.get(
        userID=current_userID, moodID=selected_mood)
    return user_ideal


def get_subset(decade, genre, current_user, selected_mood):
    """
    Gets a subset of songs similar to user's ideal from database
    based on selected mood and filtered by selected genre and decade
    """
    songs_raw = models.songs.objects.filter(year__icontains=decade, genre__icontains=genre)
    likes_raw = models.likedSongs.objects.filter(userID=current_user, moodID=selected_mood)
    idList = []
    #If the user has liked songs, get ID of liked songs
    if likes_raw.exists():
        for like in likes_raw:
            song = models.songs.objects.get(id=like.songID_id)
            idList.append(song.spotifyID)
    #Exclude songs the user has already liked
    songs = list(songs_raw.exclude(spotifyID__in=idList))
    return songs


def featurize(songs):
    # returns song list with only relevant features for recommendation
    return [[song.acousticness, song.danceability, song.energy, song.instrumentalness, song.liveness, song.mode, song.speechiness, song.tempo, song.valence, song.duration, song.songKey, song.loudness, song.popularity] for song in songs]


def recommend(survey_song, songs):
    # calculates the distance to each song in the list
    dists = cdist([survey_song], featurize(songs))[0]
    # gets the 10 clostest distances
    recommendations = heapq.nsmallest(10, dists)
    # converts distances back into their corresponding song
    recommendations = [
        songs[numpy.where(dists == item)[0][0]] for item in recommendations]

    return [song.spotifyID for song in recommendations]


def recommendLikeSong(request, songID, like):
    #Handles liking and disliking songs from recommend app

    #Retrieve values
    current_user = request.user
    selected_song = models.songs.objects.get(spotifyID=songID)
    #Determine if song is being liked or disliked
    if like == 'True':
        #Get additional values required to like
        selected_mood = models.moods.objects.get(id=request.session['moodID'])
        #Save newly liked song to database
        new_like = models.likedSongs(
            userID=current_user, moodID=selected_mood, songID=selected_song, liked=True)
        new_like.save()
        return redirect('/home/newPlaylist')
    else:
        #Find and delete disliked song from database
        disliked_song = models.likedSongs.objects.get(userID=current_user, songID=selected_song)
        disliked_song.delete()
        return redirect('/home/likedSongs')
