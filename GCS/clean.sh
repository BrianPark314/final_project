#!/bin/bash

cd /content/data/unzip

find . -depth -type d -empty -exec rmdir {} \;