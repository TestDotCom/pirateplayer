# PiratePlayer
While there are other good software for audio playing, none of them works fully offline (mopidy) or doesn't natively support GPIO buttons (omxplayer): PiratePlayer to the rescue!

# HOW-TO use
while browsing menu:
>press A to scroll up  
>press B to scroll down  
>press X to select current file  
>press Y to go back  

while playing:
>press A to stop and go back to menu  
>press B to decrease volume  
>press X to play//pause  
>press Y to increase volume  

## Hardware needs
- Raspberry pi, a cheap model like the zero-w works fine
- Pimoroni's pirate-audio hat, or hack together some DIY
- (optional) 3.7v LiPo + 5v regulator or something like a LiPo shim

## Install deps
Install requirements for [gstreamer](https://gstreamer.freedesktop.org/documentation/installing/on-linux.html) and [hifiberry dac](https://www.hifiberry.com/docs/software/configuring-linux-3-18-x)

then make sure you have installed:
>gobject-introspection libgirepository1.0-dev libcairo2-dev

## Setup dev environment
PiratePlayer runs with python >= 3.5

>$ virtualenv venv  
>$ . venv/bin/activate  
>$ pip3 install --editable .  
>$ pirateplayer  

## Install as systemd service (from dev environment)
>$ mkdir -p ~/.config/systemd/user/  
```
$ nano ~/.config/systemd/user/pirateplayer.service

[Unit]
Description=PiratePlayer Service

[Service]
WorkingDirectory={pirateplayer_path}/pirateplayer
ExecStart={pirateplayer_path}/venv/bin/python venv/bin/pirateplayer

[Install]
WantedBy=default.target
```

>$ mkdir -p ~/.config/pirateplayer/  
>$ cp {pirateplayer_path}/conf.ini ~/.config/pirateplayer/conf.ini  

>$ systemctl --user enable pirateplayer.service  
>$ systemctl --user start pirateplayer.service

## Install as systemd service (from python module)
install pirateplayer from pip (coming soon)   
launch install.sh
