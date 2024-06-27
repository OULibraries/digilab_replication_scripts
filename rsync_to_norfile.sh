#!/bin/sh

PATH=/usr/local/bin:/usr/bin:/bin:/sbin:$PATH
LOGFILE=$1
MOUNTPOINT=$2
WEBHOOK=$3



# Skip if the right filesystems aren't mounted
mountpoint $MOUNTPOINT || exit 1

# Use flock to skip if previous run is incomplete
(
  flock -x -w 10 200 || exit 1;

# rsync to move files from bagit to norfile
  rsync -az --omit-dir-times --no-perms --update --delete --log-file=$LOGFILE /srv/bagit/ /mnt/autofs/norfile/UL-BAGIT
 
  curl -X POST -H 'Content-type: application/json' --data '{"text":"Scheduled bag move from Bagit to Norfile completed successfully"}' $WEBHOOK

) 200>/var/lock/freezer_bag_cronlock-bagit
