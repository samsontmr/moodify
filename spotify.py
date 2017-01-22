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

emotions = {'neutral' : ['neutral', 'popular', 'hits', 'dance', 'hot'],
            'happiness' : ['happiness', 'happy', 'cheerful', 'summer', 'upbeat'],
            'anger' : ['angry', 'anger', 'rage', 'upset'],
            'sadness' : ['sad', 'sadness', 'emo', 'winter'],
            'fear' : ['calm', 'calming', 'relax']}

def get_playlist(emotion):
    keyword = random.choice(emotions[emotion])
    random_int = random.randint(0, 75)
    playlist_list = sp.search(keyword, limit=10, offset=random_int, type='playlist', market='SG')['playlists']['items']
    
    for pl in playlist_list:
        if pl['public'] is None or pl['public'] == True:
            return pl['external_urls']['spotify']