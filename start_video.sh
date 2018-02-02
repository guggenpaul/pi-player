#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/home/multimedia/
export MEDIA_DIR=/home/multimedia/media/
python /home/multimedia/piplayer/broadcaster.py &
python /home/multimedia/piplayer/run.py &
python /home/multimedia/piplayer/run_video.py
