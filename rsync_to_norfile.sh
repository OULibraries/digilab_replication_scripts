#!/bin/sh

PATH=/usr/local/bin:/usr/bin:/bin:/sbin:$PATH
LOGFILE=$1
MOUNTPOINT=$2
WEBHOOK=$3
ORIGIN=$4
DESTINATION=$5
LOCKFILE=$6


# Skip if the right filesystems aren't mounted
mountpoint $MOUNTPOINT || exit 1

# Use flock to skip if previous run is incomplete
(
  flock -x -w 10 200 || exit 1;

# rsync to move files from NAS to Norfile
  rsync -az --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE $ORIGIN $DESTINATION
 
  curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag move from Bagit to Norfile completed successfully"}' $WEBHOOK

) 200>$LOCKFILE
