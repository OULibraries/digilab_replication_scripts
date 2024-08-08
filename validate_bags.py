#!/usr/bin/python

import os
import pandas as pd
import sys
import bagit
from pathlib import PATH

from config import *

#send 1 bag at a time -- make a loop that contains the is.valid function
rootdir = sys.argv[1]
pp = PurePath(rootdir).root
valid_bags = []

#Path.walk iterates top-down in the root directory and assumes that the contents are unchanged. It yields a three tuple of (dirpath, dirnames, filenames )
for dirnames in Path.walk(pp):
    for subdir in dirnames:
        bags = bagit.Bag(subdir)
        for bag in bags:
            if bag.is_valid():
                bagname = pp.parts[-1]
            valid_bags.append(bagname)
            print("This is a valid bag.")
        else:
            print("This is not a valid bag")

df = pd.DataFrame(valid_bags)
df.to_csv('valid_bags.csv')

