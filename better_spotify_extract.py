import spotipy
from spotipy.oauth2 import SpotifyOAuth
import argparse
import logging

def authenticate(client_id, client_secret, redirect_uri, scope='playlist-read-private'):
    auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def get_playlist_tracks(sp, playlist_id):
    results = sp.playlist(playlist_id, fields="tracks,next")
    tracks = results['tracks']
    track_items = tracks['items']

    while tracks['next']:
        tracks = sp.next(tracks)
        track_items.extend(tracks['items'])

    return track_items

def extract_song_and_artist_names(track_items):
    song_and_artist_names = [] 
    for item in track_items:
        track = item['track']
        artist_names = ', '.join([artist['name'] for artist in track['artists']])
        song_and_artist_names.append(f"{track['name']} by {artist_names}")
    return song_and_artist_names

def save_to_file(song_and_artist_names, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in song_and_artist_names:
            f.write("%s\n" % item)

def main(client_id, client_secret, redirect_uri, username, playlist_id, filename):
    try:
        sp = authenticate(client_id, client_secret, redirect_uri)
        track_items = get_playlist_tracks(sp, playlist_id)
        song_and_artist_names = extract_song_and_artist_names(track_items)
        save_to_file(song_and_artist_names, filename)
    except Exception as e:
        logging.exception("An error occurred: ")

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Extract song and artist names from a Spotify playlist.')
    parser.add_argument('--client_id', type=str, default='8f422be7995849cbb05d4fb3ed0a38bb', help='Your Spotify application client ID.')
    parser.add_argument('--client_secret', type=str, default='195d7dc25a3147ddbed42d37a7aef406', help='Your Spotify application client secret.')
    parser.add_argument('--redirect_uri', type=str, default='https://open.spotify.com/', help='Your Spotify application redirect URI.')
    parser.add_argument('--username', type=str, default='TensorwaveEM', help='Your Spotify username.')
    parser.add_argument('--playlist_id', type=str, default='1JZt6hNyjwxvyjRzUDG73P', help='The ID of the Spotify playlist to extract songs from.')
    parser.add_argument('--filename', type=str, default='songs2.txt', help='The file to save the song and artist names to.')
    args = parser.parse_args()

    main(args.client_id, args.client_secret, args.redirect_uri, args.username, args.playlist_id, args.filename)

    # python spotify_playlist_gather.py --client_id your_client_id --client_secret your_client_secret --redirect_uri your_redirect_uri --username your_username --playlist_id your_playlist_id --filename songs.txt
