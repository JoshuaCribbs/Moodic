from django.shortcuts import render, redirect

from .models import Question
from databaseModels.models import idealSongs, moods, songs, likedSongs, surveyData


# song values for adjustment by survey
mood = 0
genre = "none"
year = 200
acousticness = 0.492
dancability = 0.548
energy = 0.481
instrumentalness = 0.000204
liveness = 0.135
loudness = -10.474
speechiness = 0.045
tempo = 114.778
valence = 0.544

#varibles for managment of the survey
choice = 0
question_index = 0

#Questions to be displayed by the survey
questions = ["How are you feeling", 
            "",
            "What genre?",
            "What Time Period?", 
            "Do you feel like talking to someone?", 
            "Calming or Energetic?",
            "What drink would you prefer?", 
            "What color apeals to you most right now?",
            "Where would you rather be?",
            "if Your mood were a Season which would it be?"]



#initial index for displaying survey
def index(request):
    global question_index
    question_index = 0
    current_question = questions[question_index]

    context = {'current_question': current_question,
               'question_index': question_index, 
    }
   
    return render(request, 'survey/SurveyPage.html', context=context)


# Method for dealing with survey results, modifying values that get sent to reccomender,
# and incrementing questions in the survey
# this method is called each time the "next" button is pressed
def increment(request):
    global question_index, mood, genre, year, acousticness, dancability, energy
    global instrumentalness, liveness, loudness, speechiness, tempo, valence
    global choice


    if question_index == 0:
        if request.method == 'POST':
            mood = request.POST.get('mood')
        if idealSongs.objects.filter(moodID= mood, userID= request.user).exists():
            question_index = question_index+1
            print("test message")
        else:
            question_index = question_index+1
            return render(request, 'survey/SongSelect.html')
    elif question_index == 2:
        if request.method == 'POST':
            genre = request.POST.get('genre')
            #Input validation of genre: reloads question if genre doesn't exist
            genre_song = songs.objects.filter(genre__icontains=genre)[:1]
            if not genre_song.exists():
                question_index = question_index-1
    elif question_index == 3:
        if request.method == 'POST':
            year = request.POST.get('Decade')
    elif question_index == 4:
        if request.method == 'POST':
            choice = request.POST.get('q5')
            print (choice)
            if choice == '1':
                speechiness += 0.1
            elif choice == '2':
                speechiness = 0.0
    elif question_index == 5:
        if request.method == 'POST':
            choice = request.POST.get('q6')
            print (choice)
            if choice == '1':
                energy -= 0.1
                dancability -= 0.1
                loudness += 5.0
                valence += 0.1
            elif choice == '2':
                energy += 0.1
                dancability += 0.1
                loudness -= 5.0
                valence -= 0.1
    elif question_index == 6:
        if request.method == 'POST':
            choice = request.POST.get('q7')
            if choice == '1':
                energy += 0.1
                valence += 0.1
            elif choice == '2':
                energy -= 0.1
                valence -= 0.1
    elif question_index == 7:
        if request.method == 'POST':
            choice = request.POST.get('q8')
            if choice == '1':
                acousticness += 0.1
                tempo -= 10.0
                energy -= 0.1
                valence -= 0.1
            elif choice == '2':
                acousticness -= 0.1
                tempo += 10.0
                energy += 0.1
                valence += 0.1
            elif choice == '3':
                acousticness += 0.1
                valence += 0.1
            elif choice == '4':
                energy += 0.1
                loudness -= 10
                valence -= 0.1
    elif question_index == 8:
        if request.method == 'POST':
            choice = request.POST.get('q9')
            if choice == '1':
                acousticness += 0.1
                energy += 0.1
            elif choice == '2':
                energy += 0.1
                speechiness += 0.1
                loudness -= 10
            elif choice == '3':
                speechiness += 0.1
                tempo += 10.0
                loudness -= 10
            elif choice == '4':
                energy -= 0.1
                loudness += 10
                tempo -= 10.0
    elif question_index == 9:
        if request.method == 'POST':
            choice = request.POST.get('q10')
            if choice == '1':
                dancability += 0.2
                speechiness += 0.2
                valence += 0.2
            elif choice == '2':
                dancability += 0.1
                speechiness += 0.1
                valence += 0.1
            elif choice == '3':
                dancability -= 0.1
                speechiness -= 0.1
                valence -= 0.1
            elif choice == '4':
                dancability -= 0.2
                speechiness -= 0.2
                valence -= 0.2

    question_index = question_index+1

    current_question = questions[question_index]
    context = {'current_question': current_question,
               'question_index': question_index,
    }
    
    return render(request, 'survey/SurveyPage.html', context=context)

# Method for ending the survey, stores values in django sessions for use by the Reccomender app
# this method is called at the end of the survey when the submit button is pressed
def Submit(request):
    global year, mood, acousticness, dancability, energy, instrumentalness, liveness, loudness, speechiness, tempo, valence

    #Save survey answers to session for retrieval by recommender system
    request.session['moodID'] = mood
    request.session['genre'] = genre
    request.session['acousticness'] = acousticness
    request.session['danceability'] = dancability
    request.session['energy'] = energy
    request.session['instrumentalness'] = instrumentalness
    request.session['liveness'] = liveness
    request.session['speechiness'] = speechiness
    request.session['tempo'] = tempo
    request.session['valence'] = valence
    request.session['loudness'] = loudness
    request.session['year'] = year
    request.session['playlist'] = []
    
    return render(request, 'survey/SComplete.html')

# Method that controls the search functionallity
# takes user input and returns a list a list of songs from the database that match the user input
# this method is called whenever the Search button is pressed
def songSelect(request):
    #Reset search results/flag
    showSongs=False
    resList = []
    #Perform search if requested
    if request.method == 'POST':
        search = request.POST.get('search')
        searchRes = songs.objects.filter(name__icontains = search)
        #If search gave results, process each spotifyID
        if searchRes.exists():
            for res in searchRes:
                resList.append(res.spotifyID)
            #Flag html that there are songs to display
            showSongs = True
    
    context = {'resList': resList,
                'showSongs': showSongs,}
    
    print(showSongs)
    return render(request, 'survey/songSelect.html', context=context)


# Method that manages the like functionallity
# when like is clicked next to a particular song, that song is stored in the database with identifing values
# for user and the previously selected mood
def surveyLikeSong(request, songID):
    #Handles liking songs from survey app

    #Retrieve values
    selected_song = songs.objects.get(spotifyID=songID)
    selected_mood = moods.objects.get(id=mood)
    current_user = request.user
    #Save liked song to database
    new_like = likedSongs(userID=current_user,moodID=selected_mood,songID=selected_song,liked=True)
    new_like.save()
    #Redirect back to search page
    return redirect('/home/survey/search')