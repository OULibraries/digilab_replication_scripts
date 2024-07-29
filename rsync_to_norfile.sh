#!/bin/sh

PATH=/usr/local/bin:/usr/bin:/bin:/sbin:$PATH
LOGFILE=$1
#mountpoint for norfile/UL-BAGIT
MOUNTPOINT=$2
WEBHOOK=$3
#origin directories NASes mounted on Norfile
ORIGIN_PRIVATE=$4
ORIGIN_SHAREOK=$5
ORIGIN_PRESERVATION=$6
LOCKFILE=$7


# Skip if the right filesystems aren't mounted
mountpoint $MOUNTPOINT || exit 1

# Use flock to skip if previous run is incomplete
(
  flock -x -w 10 200 || exit 1;

# rsync to move files from NAS to Norfile
  rsync -azv --dry-run --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE $ORIGIN_PRIVATE $MOUNTPOINT
  rsync -azv --dry-run --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE $ORIGIN_SHAREOK $MOUNTPOINT
  rsync -azv --dry-run --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE $ORIGIN_PRESERVATION $MOUNTPOINT
 
#  curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag move from Bagit to Norfile completed successfully"}' $WEBHOOK

) 200>$LOCKFILE
