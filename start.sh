#!/bin/bash
screen -X -S djeban_pub kill

script_dir=`dirname $0`
cd $script_dir

# screen -dmS djeban_bot_pub ./env/bin/python main.py
./env/bin/pip install --upgrade pip
./env/bin/pip install --upgrade -r requirements.txt
screen -dmS djeban_pub ./env/bin/python main.py
