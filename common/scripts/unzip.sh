#!/bin/sh

cd /Users/Shark/Projects/final_project/data/166.약품식별\ 인공지능\ 개발을\ 위한\ 경구약제\ 이미지\ 데이터/01.데이터/1.Training/라벨링데이터/단일경구약제\ 5000종
for file in *.zip; do
  time unzip "${file}" -d $2 && rm "${file}"
done