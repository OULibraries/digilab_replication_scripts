#!/usr/bin/python

import os
import sys
import bagit

from config import *

rootdir = sys.argv[1]

valid_bags = []

for subdir in os.walk(rootdir):
    bags = bagit.Bag(dirname)
        for bag in bags:
            if bag.is_valid():
                valid_bags.append(dirname)
        print(valid_bags)
##I want to output the valid bags list for use in the rsync.
