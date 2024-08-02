#!/bin/bash

#Executes python script to validate bags and assigns output to variable
VALID_BAGS=$(python3 validate_bags.py $NAS1)

# calls rsync_to_norfile script and passes validated bags to script
/bin/bash/ rsync_to_norfile.sh  $VALID_BAGS
