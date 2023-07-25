import spotipy
from spotipy.oauth2 import SpotifyOAuth

# replace with your own Spotify Developer details
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'your_redirect_uri'

# replace with your username and the playlist id you want to extract songs from
username = 'your_username'
playlist_id = 'your_playlist_id'

scope = 'playlist-read-private'
auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
sp = spotipy.Spotify(auth_manager=auth_manager)

results = sp.playlist(playlist_id, fields="tracks,next")

tracks = results['tracks']

song_and_artist_names = []
for item in tracks['items']:
    track = item['track']
    artist_names = ', '.join([artist['name'] for artist in track['artists']])
    song_and_artist_names.append(f"{track['name']} by {artist_names}")

print(song_and_artist_names)
