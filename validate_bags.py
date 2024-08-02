#!/usr/bin/python

import sys
import bagit

from config import *

source_path = sys.argv[1]

valid_bags = []
incomplete_bags = []

bags = bagit.Bag(source_path)
    for bag in bags:
        if bag.is_valid():
            valid_bags.append(source_path)
        else:
            incomplete_bags.append(source_path)

##I need to assign valid bags to a variable and use that in the rsync.
