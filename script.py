import sys
import requests
import spotipy
import json
import webbrowser
import time
from random import randint
from spotipy import util

username = '11186484468'
scope = 'user-top-read'

nrg = 0.0
live = 0.0
tempo = 0.0
speech = 0.0
acous = 0.0
inst = 0.0
dance = 0.0
key = 0.0
loud = 0.0
val = 0.0

LIMIT = 5

spotify_token = util.prompt_for_user_token(username, scope, client_id='f25193ec5e474898966a8a2e1cda9df2', client_secret='67d776c422b24b33b064159e39764873', redirect_uri='https://example.com/callback/')

if spotify_token:
    sp = spotipy.Spotify(auth=spotify_token)
    results = sp.current_user_top_tracks(limit=LIMIT)
    results2 = sp.current_user_top_artists(limit=LIMIT)
    tids = []
    print(json.dumps(results, indent=4))
    print(json.dumps(results2, indent=4))
    for i, t in enumerate(results['items']):
       tids.append(t['uri'])

    features = sp.audio_features(tids)
    for feature in features:
        nrg += feature['energy']
        live += feature['liveness']
        tempo += feature['tempo']
        speech += feature['speechiness']
        acous += feature['acousticness']
        inst += feature['instrumentalness']
        dance += feature['danceability']
        key += feature['key']
        loud += feature['loudness']
        val += feature['valence']

        #print(json.dumps(feature, indent=4))
    
    nrg = nrg/LIMIT
    live = live/LIMIT
    tempo = tempo/LIMIT
    speech = speech/LIMIT
    acous = acous/LIMIT
    inst = inst/LIMIT
    dance = dance/LIMIT
    key = key/LIMIT
    loud = loud/LIMIT
    val = val/LIMIT
    
    genres = sp.recommendation_genre_seeds()
    print(json.dumps(genres, indent=4))
    genreList = []
    artistList = []
    trackList = []
    for artist in results2['items']:
        artistList.append(artist['id'])
    for track in results['items']:
        trackList.append(track['id'])
    recommended = sp.recommendations(seed_artists = artistList,seed_track=trackList, target_energy = nrg, target_liveness = live, target_tempo = tempo, target_speechiness = speech, target_acousticness = acous, target_instrumentalness = inst, target_danceability = dance, limit=5)
    print(json.dumps(recommended, indent=4))
    x = randint(0,4)
    count = 0
    for i in recommended['tracks']:
        print (i['external_urls']['spotify'])
        if count == x:
            webbrowser.open_new(i['external_urls']['spotify'])
        count = count + 1
  

else:
    print ("Can't get token for", username)
