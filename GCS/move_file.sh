#!/bin/bash

cd /content/data/unzip

find . -name '*.png' -exec mv {} /content/data/train/images \;

gsutil cat gs://pill_data_brain/zip/TS_단일_42.zip | for i in $(jar --list); do gsutil cat gs://pill_data_brain/zip/TS_단일_42.zip | jar x $i && cat $i | gsutil cp - gs://pill_data_brain/unzip/$i && rm ./$i; done;
gsutil -m cat gs://pill_data_brain/zip/TS_42_단일.zip