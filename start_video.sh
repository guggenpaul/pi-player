#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/home/multimedia/
export MEDIA_DIR=/home/multimedia/media/
python /home/multimedia/pi-player/broadcaster.py &
python /home/multimedia/pi-player/run.py &
python /home/multimedia/pi-player/run_video.py
