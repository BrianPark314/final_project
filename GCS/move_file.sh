#!/bin/bash

cd /content/data/unzip

find ~/ -type f -print0 | xargs -0 mv -t /content/data/train/images