#!/bin/bash

source config
#Include logging functionality that list bagnames and their s3 URI then sync back to Norfile

#***add command or script to output bag names and URIs to file for each sync***

# sync new bags from NAS1 to S3://ul-bagit and create s3_sync.txt then append output to file from subsequent sync commands
aws s3 sync $INCLUDE_PRIVATE_ONLY_BAGIT $S3BAGIT_PRIVATE --acl private --recursive --dryrun --output text > s3_sync.txt
aws s3 sync $INCLUDE_PUBLIC_ONLY_BAGIT $S3BAGIT_SOURCE --acl private --recursive --dryrun >> s3_sync.txt

# sync new bags from NAS2 to S3://ul-bagit
aws s3 sync $INCLUDE_PRIVATE_ONLY_BAGIT2 $S3BAGIT_PRIVATE --acl private --recursive --dryrun >> s3_sync.txt
aws s3 sync $INCLUDE_PUBLIC_ONLY_BAGIT2 $S3BAGIT_SOURCE --acl private --recursive --dryrun >> s3_sync.txt



# Post notification to Slack channel digilab-replication-notifications
#curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag copy from NASes to S3 completed successfully"}' $WEBHOOK
