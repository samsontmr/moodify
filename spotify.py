# -*- coding: utf-8 -*-

import random
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

file = open("spotify_app_token.txt", 'r')
token_stuff = file.readlines()
SPOTIPY_CLIENT_ID=token_stuff[0][:-1]
SPOTIPY_CLIENT_SECRET=token_stuff[1]
file.close()

client_credentials_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#genres = sp.recommendation_genre_seeds()
#features = sp.audio_features(tracks=['http://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6'])

random_int = random.randint(0,75)

playlist_list = sp.search('angry', limit=10, offset=random_int, type='playlist', market=None)['playlists']['items']

for pl in playlist_list:
    if pl['public'] is None or pl['public'] == True:
        pl_url = pl['external_urls']['spotify']
        break
    else:
        continue

#print(pl_url)
