#!/bin/sh

cd /content/data/zip/

for file in *.zip; do
  echo ${file}
  unzip "${file}" -d "/content/data/unzip" && rm "${file}"
done