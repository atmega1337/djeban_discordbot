#!/bin/bash

mkdir -p logs/chats

screenname=$(pwd | grep -o '[^/]*$')

screen -X -S $screenname kill

script_dir=`dirname $0`
cd $script_dir

if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

./venv/bin/pip install --upgrade pip
./venv/bin/pip install --upgrade -r requirements.txt
screen -dmS $screenname ./venv/bin/python main.py
