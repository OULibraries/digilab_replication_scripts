#!/bin/bash

#rsync from NAS to Norfile with include/exclude statements
#to target source/ and private/ subsets of objects for sync
#to S3
source config
#VALID_BAGS=$1

# Check for mounted filesystem and skip if the right filesystems aren't mounted
mountpoint $MOUNTPOINT || exit 1
mountpoint $NAS1 || exit 1
mountpoint $NAS2 || exit 1

# Use flock to skip if previous run is incomplete
(
  flock -x -w 10 200 || exit 1;

#--include=private/ shareok/ preservation/ 
  rysnc -azv -f "+ */" -f "- *" --dry-run --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE --include=$VALID_BAGS $MOUNTPOINT 
  #"""insert for loop to move bags only--be careful not to overwrite bags by syncing tombstone to norfile!!!"""

#***add command to output bagnames to file for completed sync***


  #rysnc -azv --dry-run --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE --include=$INCLUDE_PUBLIC_ONLY $MOUNTPOINT

  curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag move from Bagit to Norfile completed successfully"}' $SLACK_WEBHOOK

) 200>$LOCKFILE