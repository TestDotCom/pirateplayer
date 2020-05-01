#!/bin/bash

LOCAL_CONFIG=~/.config
SERVICE_DIR=$LOCAL_CONFIG/systemd/user/
CONF_DIR=$LOCAL_CONFIG/pirateplayer/

if [ ! -d "$SERVICE_DIR" ]; then
    mkdir -p "$SERVICE_DIR"
fi

if [ ! -d "$CONF_DIR" ]; then
    mkdir -p "$CONF_DIR"
fi

if [ "$CONF_DIR/conf.ini" ]; then
    echo "resetting conf.ini to default values"
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
    echo "resetting systemd service to default values"
fi

cat <<EOF > "$SERVICE_DIR/pirateplayer.service"

[Unit]
Description=PiratePlayer Service

[Service]
ExecStart=python3 -m pirateplayer

[Install]
WantedBy=default.target

EOF

echo "to launch pirateplayer at startup do:\nsystemctl --user enable pirateplayer.service"
echo "to launch pirateplayer right now do:\nsystemctl --user start pirateplayer.service"
