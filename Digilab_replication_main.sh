#!/bin/sh

# Execute Rsync to move bags from NAS1 and NAS2 to Norfile. Creates tombstone for each and notifies 
# via Slack #digilab-replication-notifications upon successful completion.
/bin/bash /opt/<path>/rsync_to_norfile.sh

# Executes AWS S3 sync to copy bags from Norfile to S3 bucket UL-Bagit. Notifies 
# via Slack #digilab-replication-notifications upon successful completion.
/bin/bash /opt/<path>/sync_to_s3.sh
