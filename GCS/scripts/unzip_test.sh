#!/bin/sh

cd C:Users/user/Downloads/166.약품식별\ 인공지능\ 개발을\ 위한\ 경구약제\ 이미지\ 데이터/01.데이터/2.Validation/원천데이터/단일경구약제\ 5000종
mkdir $1
mkdir $2
for file in *.zip; do
    time unzip "${file}" -d $1 && rm "${file}"
    echo "${file}"
done
