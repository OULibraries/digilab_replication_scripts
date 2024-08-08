#!/usr/bin/python

import bagit
import subprocess
import os
import sys
from pathlib import Path
from config import *

nas_path = sys.argv[1]

p = Path(nas_path)
for child in p.iterdir(): child

if os.path.isdir(child):
    print(child + "is a directory.")
    bag = bagit.Bag(child)
    if bag.is_valid():
        print(child + "is a valid bag.")
        subprocess.call("./rsync_script  .sh %s" %(str(child)))
        print(child + "will be copied to Norfile")
        subprocess.call("./s3_sync_script  .sh %s" %(str(child)))
        print(child + "will be copied to S3")
    else:
        print(child + "is not a valid bag.")
else:
    print(child + "is a file.") 



    
