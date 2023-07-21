#!/bin/bash

cd /media/brian/data/unzip

gsutil -m cp -n "/media/brian/data/unzip/*/*.png" gs://pill_data_brain/train/images
