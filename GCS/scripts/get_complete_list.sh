#!/bin/sh
touch $1/complete.txt
truncate -s 0 $1/complete.txt
cd $1
gsutil ls gs://pill_data_brain/processed/train >> complete.txt