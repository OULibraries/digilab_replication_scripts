#!/bin/sh

#'''Check for files that are 0kb and append to list for exclusion. Define var that contains exclusion list. That variable can be inserted in each rsync command string'''

/bin/bash/ /opt/oulib/filesync/verify_bags.sh
# Execute Rsync to move bags from NAS1 and NAS2 to Norfile. Creates tombstone for each and notifies 
# via Slack #digilab-replication-notifications upon successful completion.

/bin/bash /opt/oulib/filesync/rsync_nas1.sh

/bin/bash /opt/oulib/filesync/rsync_nas2.sh

# Executes AWS S3 sync to copy bags from NASes to S3 bucket UL-Bagit. Notifies 
# via Slack #digilab-replication-notifications upon successful completion.
/bin/bash /opt/oulib/filesync/sync_to_s3.sh
