#!/bin/sh

cd /content/data/zip/
for f in *.zip; do unzip $f -d "/content/data/unzip"; done

for file in *.zip; do
  echo ${file}
  unzip "${file}" -d "/content/data/unzip" && rm "${file}"
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