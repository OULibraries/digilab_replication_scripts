#!/bin/sh

# Execute Rsync to move bags from NAS1 and NAS2 to Norfile. Creates tombstone for each and notifies 
# via Slack #digilab-replication-notifications upon successful completion.

/bin/bash /opt/oulib/lib-filesync/rsync_nas1.sh

/bin/bash /opt/oulib/lib-filesync/rsync_nas2.sh

# Executes AWS S3 sync to copy bags from Norfile to S3 bucket UL-Bagit. Notifies 
# via Slack #digilab-replication-notifications upon successful completion.
/bin/bash /opt/oulib/lib-filesync/s3_sync_main.sh
