#!/bin/sh
cd /content/data/zip/

for file in *.zip; do
  unzip "${file}" -d "/content/data/unzip" && rm "${file}"
done