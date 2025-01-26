#!/bin/bash

mkdir -p logs/chats

screenname=$(pwd | grep -o '[^/]*$')

screen -X -S $screenname kill

script_dir=`dirname $0`
cd $script_dir

./.env/bin/pip install --upgrade pip
./.env/bin/pip install --upgrade -r requirements.txt
screen -dmS $screenname ./.env/bin/python main.py
