#!/bin/bash

'''executes the python script to find, validate, rsync to norfile,
   and upload to S3 each bag given a source path on a NAS
'''

python findAndUploadBags.py --sourcePath /mnt/NAS2/Bagit2/private/ --bucket ul-bagit --rsyncDest /mnt/norfile/UL-BAGIT/private/ &> "private_$(date +%Y-%m-%d.txt)"
