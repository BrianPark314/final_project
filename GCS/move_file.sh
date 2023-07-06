#!/bin/bash

cd /content/data/unzip

find ~/ -name '*.png' -print0 | xargs -0 mv -t /content/data/bash_test