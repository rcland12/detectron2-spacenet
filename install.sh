#!/bin/bash

source download.sh
echo "Done downloading SpaceNet dataset. Now converting TIF images to PNG."

python convert_tif.py
echo "Done converting TIF images to PNG. Now creating JSON files for Detectron2"

python create_jsons.py
echo "Done creating JSON files. Have fun with Detectron2!"
