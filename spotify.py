# -*- coding: utf-8 -*-

import random
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

keys = dict([line.split() for line in open('keys')])
SPOTIPY_CLIENT_ID = keys['SpotifyID']
SPOTIPY_CLIENT_SECRET = keys['SpotifySecret']


client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#genres = sp.recommendation_genre_seeds()
#features = sp.audio_features(tracks=['http://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6'])

def get_playlist(emotion):
    if emotion == 'neutral':
        emotion = 'popular'
    random_int = random.randint(0, 75)
    playlist_list = sp.search(emotion, limit=10, offset=random_int, type='playlist', market=None)['playlists']['items']
    
    for pl in playlist_list:
        if pl['public'] is None or pl['public'] == True:
            return pl['external_urls']['spotify']