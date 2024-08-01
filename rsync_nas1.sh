#!/bin/bash

#Check for files that are 0kb and append to list for exclusion.
/bin/bash/ verify_bags.sh $NAS1

# calls rsync_to_norfile script and passes Logfile and Mount variable arguments for nas1
/bin/bash/ rsync_to_norfile.sh  $INCLUDE_PRIVATE_ONLY_BAGIT $INCLUDE_PUBLIC_ONLY_BAGIT
