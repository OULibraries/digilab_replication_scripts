#!/bin/bash

#Check for files that are 0kb and append to list for exclusion.
/bin/bash/ verify_bags.sh $NAS2

# calls rsync_to_norfile script and passes Logfile and Mount variable arguments for nas2
/bin/bash/ rsync_to_norfile.sh  $INCLUDE_PRIVATE_ONLY_BAGIT2 $INCLUDE_PUBLIC_ONLY_BAGIT2