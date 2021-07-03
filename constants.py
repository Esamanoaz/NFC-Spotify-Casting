# Edit this file

#cookies
'''
Follow the instructions at https://github.com/enriquegh/spotify-webplayer-token
to get the below cookies
'''
SP_DC = 'replace this string with the SP_DC cookie'
SP_KEY = 'replace this string with the SP_KEY cookie'

#Spotify app
'''
CLIENT_ID and CLIENT_SECRET can be created by making a new app on https://developer.spotify.com/
The REDIRECT_URI could be any URL, but it is recommened you keep it as http://localhost:8888/callback/
The REDIRECT_URI should be the same one that is on your Spotify app
'''
CLIENT_ID = 'replace this with the client ID'
CLIENT_SECRET = 'replace this with the client secret'
REDIRECT_URI = 'http://localhost:8888/callback/'

#user
'''
Your normal Spotify account username. The account should be premium, not free.
'''
USERNAME = 'replace this with your Spotify account username'

#chromecast
'''
CAST_NAME: The name of your chromecast device.
CAST_IP: The IP address of your device.
If the device can not be found with the name, it will try again with the IP.
You can find the IP address and name in the Google Home app.
'''
CAST_NAME = 'replace this with the cast name. For example: Bedroom Speaker'
CAST_IP = 'replace this with the cast IP address'

#nfc settings
'''
BEEP: True means the NFC reader beeps
      False means it does not
PATH: Leave this as is unless you have path errors.
      The following comment was taken from my code in this pull request: https://github.com/hankhank10/vinylemulator/pull/6

#if you are getting errors saying your nfc reader can not be found do the following:
#type lsusb into a terminal on your raspberry pi and enter
#in the output, find your nfc reader and copy the hex code next to it
#(for example, for the ACR122U it is 072f:2200)
#then replace 'usb' with 'usb:072f:2200'
#(or whatever lsusb outputted for your nfc reader)
'''
BEEP = True
PATH = 'usb'

#app settings
'''
ALLOW_EXPLICIT: Should explicit content be allowed? Note, this feature doesn't actually work yet.
SHUFFLE_DEFAULT: Should shuffle be on for albums?
PLAYLIST_SHUFFLE: Should shuffle be on for playlists?
'''
ALLOW_EXPLICIT = True
SHUFFLE_DEFAULT = False
PLAYLIST_SHUFFLE = True

#important variables
'''
The SCOPE variable should not be changed.
The program could stop working and ask to log back in if SCOPE is changed.
'''
SCOPE = 'user-library-read user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-modify-private'

VERSION = '1.6.2'
UPDATE_DATE = '7/3/2021'