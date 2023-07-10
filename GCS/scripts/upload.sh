#!/bin/bash

cd /Volumes/data/unzip

gsutil -m cp -n -r /Volumes/data/unzip/*/*.png gs://pill_data_brain/train/images
