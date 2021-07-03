#!/bin/bash
# Starts up the NFC casting program.
# This file should be set to executable and
# located in the default directory.

# The directory on this line should be changed to the location
# of the file nfc_casting.py on the raspberry pi.
cd /home/pi/Desktop/nfc-casting/

echo -n "Show debug? (yn)"
read VAR

if [[ $VAR = "y" ]]
then
	sudo python3 nfc_casting.py --show-debug
fi

if [[ $VAR = "n" ]]
then
	sudo python3 nfc_casting.py
fi
