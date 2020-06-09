#!/bin/bash

LOCAL_CONFIG=~/.config
SERVICE_DIR=$LOCAL_CONFIG/systemd/user/
CONF_DIR=$LOCAL_CONFIG/pirateplayer/

printf "check README for necessary system dependencies"
printf "remember to install pirateplayer from pip as user (if you haven't done it yet)\n"

if [ ! -d "$SERVICE_DIR" ]; then
    mkdir -p "$SERVICE_DIR"
fi

if [ ! -d "$CONF_DIR" ]; then
    mkdir -p "$CONF_DIR"
fi

if [ "$CONF_DIR/conf.ini" ]; then
    printf "resetting conf.ini to default values\n"
fi

cat <<EOF > "$CONF_DIR/conf.ini"

[PLAYER]
root = ~/Music

[BUTTON]
a = 5
b = 6
x = 16
y = 20

EOF

if [ "$SERVICE_DIR/pirateplayer.service" ]; then
    printf "resetting systemd service to default values\n"
fi

cat <<EOF > "$SERVICE_DIR/pirateplayer.service"

[Unit]
Description=PiratePlayer Service

[Service]
ExecStart=/usr/bin/pirateplayer

[Install]
WantedBy=default.target

EOF

printf "to launch pirateplayer at startup do:\n\tsystemctl --user enable pirateplayer.service\n"
printf "to launch pirateplayer right now do:\n\tsystemctl --user start pirateplayer.service\n"
