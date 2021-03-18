import configparser

import spotipy
from spotipy.oauth2 import SpotifyOAuth

config = configparser.ConfigParser()
config.read('config.cfg')
client_id="2d0aa7b1e8e34e6db2bbcc9e35fd4db5"
client_secret="264330e29b1143f28800cc39b0ab8007"
scope = "user-read-playback-state,user-modify-playback-state,streaming"

auth = SpotifyOAuth(
            client_id="2d0aa7b1e8e34e6db2bbcc9e35fd4db5",
            client_secret="264330e29b1143f28800cc39b0ab8007",
            redirect_uri="http://google.com/",
            scope=scope)

token = auth.get_access_token(as_dict=False)
spotify = spotipy.Spotify(auth=token)

devices = spotify.devices()
device_id = devices['devices'][0]['id']

track = spotify.search(input('Track: '))['tracks']['items'][0]['uri']
print(track)

spotify.start_playback(uris=[track], device_id=device_id)