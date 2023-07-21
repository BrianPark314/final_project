#!/bin/sh
touch $1/processed.txt
truncate -s 0 $1/processed.txt
cd $1
gsutil ls gs://pill_data_brain/processed/train/*.png >> processed.txt