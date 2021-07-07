# NFC Spotify Casting

## Description
 Inspired by [vinyl-emulator](https://github.com/hankhank10/vinylemulator). Hankhank's original version can be seen in [this Reddit post](https://www.reddit.com/r/Python/comments/he081v/i_wrote_a_python_script_to_play_an_album_on_sonos/). Plays Spotify albums, playlists, and podcasts on any Google Home speaker or Chromecast. Spotify URIs are stored on NFC tags that are stuck on the back of printed album covers (or whatever image/art you want). Tapping the album art on the NFC reader plays the album, playlist, or podcast.

## Materials needed
* A Raspberry Pi with a connection to the internet.
* Python 3.6 or greater installed on the Raspberry pi.
* A Google Assistant enabled speaker or Chromecast device.
* A premium Spotify account.
* An NFC reader. I used the ACR122U.
* NFC tag stickers. I used the NTAG215 stickers.
* Something to put the NFC tag stickers onto (album art).
* Software to write the URIs to the NFC tags. I used the free NFC tools app on Android.

## Instructions
1. Download this repository onto the Raspberry Pi. You can do this using git clone in a command line or going to the repo page and clicking code -> download zip -> and then extract the files to your desktop.
2. Follow the commented instructions in `constants.py` and fill out the file.
3. Edit line 8 in `startup.sh` so that it changes directory to the correct path.
4. Install the following Python packages with this command: `sudo pip3 install -U package-name-here`
    1. `nfcpy`
    2. `pychromecast`
    3. `spotify-token`
    4. `spotipy`
5. Write Spotify URIs to NFC tags and apply them to whatever you chose, like album art. Spotify URIs can be found in the Spotify desktop app by right clicking the three dots next to an album, playlist, or show -> click share -> hold down the alt key on Windows or command key on Mac -> click the newly shown Copy Spotify URI button.
6. Set the file `startup.sh` to an executable. You can do this by typing `sudo chmod +x pathto/filename` in the terminal.
7. The Spotify app usually needs to be open on the cast device before running the program. If it has Google assitant just say `Hey Google, play music on Spotify.` 
8. Type `./startup.sh` into the Raspberry Pi terminal.
9. Type `y` if you want debugging enabled or `n` if you don't.
10. Touch a tag to the NFC reader and take it off the reader after a second or too. Enjoy!
