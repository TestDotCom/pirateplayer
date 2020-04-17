# PiratePlayer
Offline audio player for pirate-audio hats

# HOW-TO use
while browsing menu:
- press A to scroll up
- press B to scroll down
- press X to select current file
- press Y to go back

while playing:
- press A to stop and go back to menu
- press B to decrease volume
- press X to play//pause
- press Y to increase volume

## Requirements
Raspberry pi, a cheap model like the zero-w works fine
Pimoroni's pirate-audio hat, or hack together some DIY
(optional) 3.7v LiPo + 5v regulator

## install deps
https://gstreamer.freedesktop.org/documentation/installing/on-linux.html
https://www.hifiberry.com/docs/software/configuring-linux-3-18-x

then make sure you have installed 'libatlas-base-dev'

## setup dev environment
$ virtualenv venv  
$ . venv/bin/activate  
$ pip install --editable .  
$ pirateplayer  
