#!/bin/bash

#checks if object is a directory

#for files, checks size. If size is 0kb, the name is added to catalog directory
#catalog/ is excluded from rsync

#add functionality at the last step to remove the text files generated for bags and file
#as a check of successful run
source config

ORIGIN=$1
arrBags=("")
arrFiles=("")

for i in $ORIGIN;
    #if object is a directory
    if [ -d $i ]; then
        python3 validate_bags.py $i
#I want to return the output of validate_bags.py to the correct array and then assign these as variables to include/exclude for rsync
        arrBags+=("$i")
    else:
        arrFiles+=("$i")
fi
