#!/bin/bash

#checks if object is a directory

#for files, checks size. If size is 0kb, the name is added to catalog directory
#catalog/ is excluded from rsync

#add functionality at the last step to remove the text files generated for bags and file
#as a check of successful run
source config.txt

ORIGIN=$1
arrBags=("")
arrFiles=("")

for i in $ORIGIN;
    #if object is a directory
    if [ -d $i ]
        arrBags+=("$i")
        for bag in "${arrBags[@]}"
            echo $bag > $MOUNTPOINT/"bags_to_sync.txt";
    #if file is >0kb
    elif [-s $i]
        arrFiles+=("$i")
            for file in "${arrFiles[@]}"
                echo $file > $MOUNTPOINT/"files_to_sync.txt";
    #if file is 0kb
    else
        mv $i $CATALOG
            echo "Moving 0kb files $1 to catalog";
fi
