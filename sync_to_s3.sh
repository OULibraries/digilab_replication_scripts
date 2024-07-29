#!/bin/bash

BAGIT=$1
BAGIT2=$2
S3BAGIT=$3

# sync new bags from NAS1 to S3://ul-bagit
aws s3 sync $BAGIT $S3BAGIT --acl private --recursive --dryrun

# sync new bags from NAS2 to S3://ul-bagit
aws s3 sync $BAGIT $S3BAGIT --acl private --recursive --dryrun

# Post notification to Slack channel digilab-replication-notifications
#curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag copy from NASes to S3 completed successfully"}' $WEBHOOK
