#!/bin/bash

'''executes the python script to find, validate, rsync to norfile,
   and upload to S3 each bag given a source path on a NAS
'''

python findAndUploadBagsSource.py --sourcePath /mnt/NAS2/Bagit2/ --bucket ul-bagit --syncDest /mnt/norfile/UL-BAGIT/source/ &> "source_$(date +%Y-%m-%d.txt)" 
