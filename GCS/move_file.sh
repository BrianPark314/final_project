#!/bin/bash

cd /content/data/unzip
for file in *.png; do
    mv "${file}" -v "/content/data/train/images/${file}"
done