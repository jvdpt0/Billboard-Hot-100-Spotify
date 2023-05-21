import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIFY_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIFY_SECRET')
SPOTIPY_REDIRECT_URI = os.environ.get('REDIRECT_URI')
scope = 'playlist-modify-private'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))
user_id = sp.current_user()['id']

date = input('Which data do you want to travel to? Type it in this format YYYY-MM-DD: ')
year = date[0:4]
response = requests.get('https://www.billboard.com/charts/hot-100/'+date)   
soup = BeautifulSoup(response.text, 'html.parser')

songs = soup.select('li  ul li h3')
song_list = [song.getText().strip() for song in songs]

song_uris=[]
for song in song_list:
    result = sp.search(q=f"track: {song} year: {year}", type="track")
    try:
        uri=result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print('Song not available on Spotify, skipping')

playlist = sp.user_playlist_create(user=user_id, name=date +' Billboard 100', public=False)
sp.playlist_add_items(playlist['id'], song_uris)