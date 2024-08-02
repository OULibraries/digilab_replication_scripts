#!/bin/bash

source config
#Include logging functionality that list bagnames and their s3 URI then sync back to Norfile

# sync new bags from NAS1 to S3://ul-bagit
aws s3 sync $INCLUDE_PRIVATE_ONLY_BAGIT $S3BAGIT_PRIVATE --acl private --recursive --dryrun
aws s3 sync $INCLUDE_PUBLIC_ONLY_BAGIT $S3BAGIT_SOURCE --acl private --recursive --dryrun

# sync new bags from NAS2 to S3://ul-bagit
aws s3 sync $INCLUDE_PRIVATE_ONLY_BAGIT2 $S3BAGIT_PRIVATE --acl private --recursive --dryrun
aws s3 sync $INCLUDE_PUBLIC_ONLY_BAGIT2 $S3BAGIT_SOURCE --acl private --recursive --dryrun

# Post notification to Slack channel digilab-replication-notifications
#curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag copy from NASes to S3 completed successfully"}' $WEBHOOK
