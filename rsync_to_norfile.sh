#!/bin/bash

#rsync from NAS to Norfile with include/exclude statements
#to target source/ and private/ subsets of objects for sync
#to S3
source config
INCLUDE_PRIVATE_ONLY=$1
INCLUDE_PUBLIC_ONLY=$2
# Check for mounted filesystem and skip if the right filesystems aren't mounted
mountpoint $MOUNTPOINT || exit 1
mountpoint $NAS1 || exit 1
mountpoint $NAS2 || exit 1

# Use flock to skip if previous run is incomplete
(
  flock -x -w 10 200 || exit 1;

#--include=private/ shareok/ preservation/ 
  rysnc -azv --dry-run --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE --include=$INCLUDE_PRIVATE_ONLY $MOUNTPOINT 
  #"""insert for loop to move bags only--be careful not to overwrite bags by syncing tombstone to norfile!!!"""

  rysnc -azv --dry-run --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE --include=$INCLUDE_PUBLIC_ONLY $MOUNTPOINT

  curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag move from Bagit to Norfile completed successfully"}' $SLACK_WEBHOOK

) 200>$LOCKFILE