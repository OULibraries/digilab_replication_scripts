#!/bin/bash

# sync new bags from Norfile to S3://<>/UL-Bagit--IF they came from nas1 they go to ul-bagit/private/
aws s3 sync [options] <path from norfile> s3://ul-bagit/private/

# sync new bags from Norfile to S3://<>/UL-Bagit--IF they came from nas2 they go to ul-bagit/source/
aws s3 sync <path from norfile> s3://ul-bagit/source/

# Post notification to Slack channel digilab-replication-notifications
curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag copy from Norfile to S3 completed successfully"}' $WEBHOOK