#!/bin/sh


echo "loading virtual environment"
. /opt/env/live/bin/activate

cd /opt/env/live/config

echo "starting bot"

python /opt/env/live/app/osticket_bot.py
