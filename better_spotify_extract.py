import spotipy
from spotipy.oauth2 import SpotifyOAuth
import argparse
# python script.py --client_id your_client_id --client_secret your_client_secret --redirect_uri your_redirect_uri --username your_username --playlist_id your_playlist_id
def authenticate(client_id, client_secret, redirect_uri, scope='playlist-read-private'):
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def get_playlist_tracks(sp, playlist_id):
    results = sp.playlist(playlist_id, fields="tracks,next")
    return results['tracks']['items']

def extract_song_and_artist_names(track_items):
    song_and_artist_names = []
    for item in track_items:
        track = item['track']
        artist_names = ', '.join([artist['name'] for artist in track['artists']])
        song_and_artist_names.append(f"{track['name']} by {artist_names}")
    return song_and_artist_names

def main(client_id, client_secret, redirect_uri, username, playlist_id):
    sp = authenticate(client_id, client_secret, redirect_uri)
    track_items = get_playlist_tracks(sp, playlist_id)
    song_and_artist_names = extract_song_and_artist_names(track_items)

    print(song_and_artist_names)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract song and artist names from a Spotify playlist.')
    parser.add_argument('--client_id', type=str, default='your_default_client_id', help='Your Spotify application client ID.')
    parser.add_argument('--client_secret', type=str, default='your_default_client_secret', help='Your Spotify application client secret.')
    parser.add_argument('--redirect_uri', type=str, default='your_default_redirect_uri', help='Your Spotify application redirect URI.')
    parser.add_argument('--username', type=str, default='your_default_username', help='Your Spotify username.')
    parser.add_argument('--playlist_id', type=str, default='your_default_playlist_id', help='The ID of the Spotify playlist to extract songs from.')
    args = parser.parse_args()

    main(args.client_id, args.client_secret, args.redirect_uri, args.username, args.playlist_id)
