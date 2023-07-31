#!/bin/sh
touch $1/uploaded.txt
truncate -s 0 $1/uploaded.txt
cd $1
gsutil ls "gs://pill_data_brain/train/images/**.png" >> uploaded.txt