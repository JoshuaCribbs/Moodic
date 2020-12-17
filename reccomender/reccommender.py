"""
this file should take in a song and a list of songs as input. It will return the 10 songs in the list
closest to the features of the single song
"""

from scipy.spatial.distance import cdist
import numpy
import heapq
import pandas



def recommend(survey_song, songs):
    #calculates the distance to each song in the list
    dists = cdist([survey_song], featurize(songs))[0]
    #gets the 10 clostest distances
    playlist = heapq.nsmallest(10, dists)
    #converts distances back into their corresponding song
    playlist = [songs[numpy.where(dists==item)[0][0]] for item in playlist]
    return [song[6] for song in playlist]

def featurize(songs):
    return [[song[0], song[0], song[2], song[3], song[4], song[5], song[7], song[8], song[9], song[10], song[11], song[13], song[15], song[16], song[17], song[18]] for song in songs]

#dummy method to read in the songs that are in the data base from the csv (don't use)
def readCsv():
    data = pandas.read_csv("/Users/colinlambe/PycharmProjects/SeniorProject/MoodPlaylist/database/data-2.csv")
    #data.drop(columns=['artists', 'id', 'name', 'release_date'], axis=1, inplace=True)
    return data.values.tolist()


#test test
if __name__ == "__main__":
    #songs = [[4, 9, 6], [7, 4, 6], [6, 3, 4], [4, 9, 3], [7, 6, 9], [3, 8, 2], [5, 5, 5], [8, 4, 9], [1, 3, 8], [1, 9, 1]]
    songs = readCsv()
    test_song = featurize([songs[0]])[0]
    print(recommend(test_song, songs))
