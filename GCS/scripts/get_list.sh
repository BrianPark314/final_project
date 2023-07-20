#!/bin/sh
touch $1/log.txt
truncate -s 0 $1/log.txt
cd $1
gsutil ls gs://pill_data_brain/train/images >> log.txt