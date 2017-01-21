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

neutral_cats = ['neutral', 'popular', 'hits', 'dance', 'hot']
happy_cats = ['happiness', 'happy', 'cheerful', 'summer', 'upbeat']
angry_cats = ['angry', 'anger', 'rage', 'upset']
sad_cats = ['sad', 'sadness', 'emo']
fear_cats = ['calm', 'calming', 'relax']

def get_playlist(emotion):
    if emotion == 'neutral':
        keyword = random.choice(neutral_cats)
    elif emotion == 'happiness':
        keyword = random.choice(happy_cats)
    elif emotion == 'sadness':
        keyword = random.choice(sad_cats)
    elif emotion == 'anger':
        keyword = random.choice(angry_cats)
    else:
        keyword = random.choice(fear_cats)
    random_int = random.randint(0, 75)
    playlist_list = sp.search(keyword, limit=10, offset=random_int, type='playlist', market='SG')['playlists']['items']
    
    for pl in playlist_list:
        if pl['public'] is None or pl['public'] == True:
            return pl['external_urls']['spotify']