'''
Handles connecting to a chromecast device and playing music on the device via Spotify
'''

import argparse
import logging
import sys
import time
import os
import nfc
from random import shuffle

import pychromecast
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import constants

CAST_NAME = constants.CAST_NAME
CAST_IP = constants.CAST_IP

SP_DC = constants.SP_DC
SP_KEY = constants.SP_KEY
CLIENT_ID = constants.CLIENT_ID
CLIENT_SECRET = constants.CLIENT_SECRET
SPOTIPY_REDIRECT_URI = constants.REDIRECT_URI
SPOTIFY_USERNAME = constants.USERNAME

ALLOW_EXPLICIT = constants.ALLOW_EXPLICIT
SHUFFLE_DEFAULT = constants.SHUFFLE_DEFAULT
PLAYLISTS_SHUFFLE = constants.PLAYLIST_SHUFFLE

parser = argparse.ArgumentParser(description="Cast songs/albums to Google Home via nfc controls")
parser.add_argument("--show-debug", help="Enable debug log", action="store_true")
parser.add_argument("--cast", help='Name of cast device (default: "%(default)s")', default=CAST_NAME)
parser.add_argument("--cast-ip", help='IP address of cast device (default: "%(default)s")', default=CAST_IP)
args = parser.parse_args()

if args.show_debug:
    logging.basicConfig(level=logging.DEBUG)

print('Version: ' + constants.VERSION)
print('Last updated: ' + constants.UPDATE_DATE)

def n():
    '''
    prints a new line
    '''
    print("")


def isSameSongPlaying(dictionary, tag_uri):
    '''
    returns True if the same song is playing and False if it is not.
    
    params:
        dictionary: dictionary returned from "client.current_playback('US')"

        tag_uri: the URI of the song being comapared to the currently playing song
    '''
    try:
        if dictionary == None: #If no song is playing
            return False

        context_dictionary = dictionary.get('context')
        #if context_dictionary == None:
        #    return False
        current_uri = context_dictionary.get('uri')
        #if current_uri == None:
        #    return False

        if current_uri == tag_uri: #If the song is playing
            return True
        else: #If a different song is playing
            return False
    except:
        print('\nThere was an error calling the function isSameSongPlaying.\n')
        return False


def find(string, search_term):
    '''
    returns True if 'search_term' is found anywhere in 'string'
    '''
    if string.find(search_term) != -1:
        return True
    else:
        return False


def construct_uris(dictionary, t):
    '''
    finds all the tracks in an album and returns a list of track uris

    params:
        dictionary: dictionary returned from "client.album_tracks()"

        t: type (album or playlist)
    '''
    tracks = []
    items = dictionary.get('items')
    if t == 'album':
        for item in items:
            tracks.append(item.get('uri'))
    elif t == 'playlist':
        for item in items:
            tracks.append(item.get('track').get('uri'))
    return tracks


chromecasts, browser  = pychromecast.get_listed_chromecasts(friendly_names=[args.cast])
home = None
for _cast in chromecasts:
    if _cast.name == args.cast:
        home = _cast
        break

if not home:
    print('No chromecast with name "{}" discovered'.format(args.cast))
    print("Discovered casts: {}".format(chromecasts))
    print("Attempting to connect to cast device via IP")
    n()
    home = pychromecast.Chromecast(args.cast_ip)

    if not home:
        print("Failure. Exiting.")
        sys.exit(1)
    else:
        print("Success!")
        n()

print("cast {}".format(home))

home.wait() # Start a new worker thread/wait for connection

# Log device and status
n()
print(home.device)
n()
print(home.status)
n()

spotify_device_id = None

# Create a spotify client
_scope = constants.SCOPE

#auth=access_token, 
client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=_scope, redirect_uri=SPOTIPY_REDIRECT_URI, username=SPOTIFY_USERNAME))
if args.show_debug:
    spotipy.trace = True
    spotipy.trace_out = True

# Query spotify for active devices
devices_available = client.devices()

# Get a list of available Spotify devices and ask the user which one to use
devices = devices_available['devices']
for i, device in enumerate(devices):
    print(f'{i} -> Name: {device["name"]}, \nFull device info: {device}\n')

device_choice = input('Enter the number of the device you want to use: ')
spotify_device_id = devices[device_choice]['id']

#Set up NFC reader
try:
    n()
    print('Setting up the NFC reader')
    reader = nfc.ContactlessFrontend(constants.PATH)
    print(reader)
    n()
except IOError as err:
    n()
    print('---------------')
    n()
    print(f'IOError: {err}')
    n()
    print('The NFC reader has not been found.')
    print('This error will most-likely be resolved by changing the value of the PATH variable in constants.')
    print('Check the constants.py file documentation for more information on that.')
    n()
    sys.exit(1)

def get_record(tag_data):
    #explicit_filter = ALLOW_EXPLICIT

    if tag_data.ndef:
        for record in tag_data.ndef.records:
            nfc_data = record.text
            print('Read from NFC tag: ' + record.text)

            if type(nfc_data) == type('string-example'):
                if nfc_data.startswith('spotify'):
                    playback_data = client.current_playback('US')
                    #if not isSameSongPlaying(playback_data, nfc_data):
                    try:
                        if find(nfc_data, 'album'):
                            album_info = client.album_tracks(album_id=nfc_data, market='US')
                            album_tracks = construct_uris(album_info, 'album')
                            if not isSameSongPlaying(playback_data, album_tracks[0]):
                                if SHUFFLE_DEFAULT:
                                    shuffle(album_tracks)
                                client.start_playback(device_id=spotify_device_id, uris=album_tracks, offset={'position': 0})
                                n()
                                print(f'Succesfully started playback of \n{album_tracks}')
                            else:
                                print('The album is already playing.')
                        elif find(nfc_data, 'playlist'):
                            playlist_info = client.playlist_tracks(playlist_id=nfc_data, market='US')
                            playlist_tracks = construct_uris(playlist_info, 'playlist')
                            if not isSameSongPlaying(playback_data, playlist_tracks[0]):
                                if PLAYLISTS_SHUFFLE:
                                    shuffle(playlist_tracks)
                                client.start_playback(device_id=spotify_device_id, uris=playlist_tracks, offset={'position': 0})
                                n()
                                print(f'Succesfully started playback of playlist\n{playlist_tracks}')
                            else:
                                print('The playlist is already playing.')
                        elif find(nfc_data, 'show'):
                            client.start_playback(device_id=spotify_device_id, context_uri=nfc_data)
                            n()
                            print(f'Succesfully started playback of podcast\n{nfc_data}')
                    except Exception as err:
                        reader.close()
                        n()
                        print(err)
                        input('Press enter to exit...')
                        sys.exit(0)
            
                time.sleep(0.1)

    else:
        n()
        print("The NFC reader could not read this tag.")
        n()
        print("This may be because:")
        print("- You are using a Mifare Classic NFC tag, which is not supported by your reader.")
        print("- The NFC tag you are trying to read is not storing URI's or commands at text.")


# Start playback
while True:
    reader.connect(rdwr={'on-connect': get_record, 'beep-on-connect': constants.BEEP})

# Shut down discovery
pychromecast.discovery.stop_discovery(browser)