#!/usr/bin/python

import bagit
import subprocess
import os
import sys
from pathlib import Path
from config import *

if os.path.isdir('path to object'):
    print("%s" + "is a directory.")
else:
    print("%s" + "is not a directory.")

bag = bagit.Bag('path to object')
if bag.is_valid():
    print("%s" + "is a valid bag.")
    subprocess.call(["rsync", "-avz", "--update", "--no-perms", "--omit-dir-times", "--logfile=$LOGFILE", "$MOUNTPOINT"])
    subprocess.call(["aws s3 sync", "path to object", "s3 uri", "--recursive"])
else:
    print("%s" + "is not a bag.")

