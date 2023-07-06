#!/bin/bash

cd /content/data/unzip

find . -name '*.png' -exec mv {} /content/data/train/images \;

