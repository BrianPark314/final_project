#!/bin/sh
touch /media/brian/data/log.txt

cd /media/brian/data/166.약품식별\ 인공지능\ 개발을\ 위한\ 경구약제\ 이미지\ 데이터/01.데이터/1.Training/원천데이터/단일경구약제\ 5000종

for file in *.zip; do
  time unzip "${file}" -d "/media/brian/data/unzip" && date >> /media/brian/data/log.txt && printf "${file}\n" >> /media/brian/data/log.txt && rm "${file}"
done

# gcloud dataflow jobs run decompress_test \
#     --gcs-location gs://dataflow-templates-us-central1/latest/Bulk_Decompress_GCS_Files \
#     --region Multi-region \
#     --parameters \
# inputFilePattern=gs://pill_data_brain/zip/*.zip,\
# outputDirectory=gs://pill_data_brain/unzip,\
# outputFailureFile=gs://pill_data_brain/

# gsutil cat gs://pill_data_brain/zip/TS_42_단일.zip | for i in $(jar --list); do gsutil cat gs://pill_data_brain/zip/TS_42_단일.zip | jar x $i && cat $i | gsutil cp - gs://pill_data_brain/unzip/$i && rm ./$i; done;
# gsutil -m cat gs://pill_data_brain/zip/TS_42_단일.zip
