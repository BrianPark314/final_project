#!/bin/bash

rm -rfv $3 && mkdir $3

cat $3/temp.txt | gsutil -m cp -I $2