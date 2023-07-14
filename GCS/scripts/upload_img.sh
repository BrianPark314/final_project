#!/bin/bash
touch $1/logs/complete.txt
cd $1
for file in *.png; do
    gsutil mv ${file} $2 && printf "${file}" >> complete.txt
done

printf "\n" >> complete.txt