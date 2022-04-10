#!/usr/bin/env python3

import boto3
import os
import csv
from collections import Counter
import sys

# User provides a list of batches
batch = [
    sys.argv[0],
    sys.argv[1],
    sys.argv[2]
]

# Creating Variables
s3 = boto3.resource('s3')
bucket = s3.Bucket("Bucket_Name")
work_dir = 'Your_Work_Dir'

# Loop for searching .tcv files in s3 bucket with prefix
# Downloading founded files
for x in batch:
    prefix_name = 'folder/{0}/{0}_folder'.format(x)
    for buck in bucket.objects.filter(Prefix=prefix_name):
        if buck.key.endswith('file_name.tsv'):
            dynamic_name = buck.key.split('/')[3]
            local_dir = os.path.join(work_dir, buck.key.split('/')[3])
            bucket.download_file(buck.key, local_dir)
            print('Finished downloading - ', local_dir)
            dynamic_tsv_name = '{0}'.format(dynamic_name)
            print(dynamic_tsv_name)
            with open(dynamic_tsv_name) as InputFile, open('output_file.tsv', 'a') as OutputFile:
                reader = csv.reader(InputFile, delimiter="\t", quotechar='"')
                writer = csv.writer(OutputFile)
                writer.writerow(["Batch", "ID", "Sample"])
                count_list = []
                for row in reader:
                    if row[8] != '1.0000000':
                        sample_id = row[4]
                        base_sample_id = sample_id[0:8]
                        count_list.append(sample_id)
                        counter = Counter(count_list)
                for features in counter.items():
                    final_row = str(features).replace("(", "").replace(")", "").replace("'", "")
                    writer.writerow([dynamic_tsv_name[0:12], final_row[0:8], final_row])
            with open(dynamic_tsv_name) as InputFile,  open('output_file_2.tsv', 'a') as OutputFile:
                reader = csv.reader(InputFile, delimiter="\t", quotechar='"')
                writer = csv.writer(OutputFile)
                writer.writerow(["Batch", "ID", "Sample"])
                count_list = []
                for row in reader:
                    if row[8] != '1.0000000':
                        sample_id = row[4]
                        base_sample_id = sample_id[0:8]
                        count_list.append(sample_id)
                        counter = Counter(count_list)
                for features in counter.items():
                    if features[1] >= 8:
                        final_row = str(features).replace("(", "").replace(")", "").replace("'", "")
                        writer.writerow([dynamic_tsv_name[0:12], final_row[0:8], final_row])
                os.remove(dynamic_tsv_name)
