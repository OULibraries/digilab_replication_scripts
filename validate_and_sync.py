!#/usr/bin/python

import bagit
import subprocess
import os
import sys
from config import *

path = sys.argv[1]

if os.path.isdir(path):
    print(path+ "is a directory.")
    bag = bagit.Bag(path)
    if bag.is_valid():
        print(path + "is a valid bag.")
        subprocess.check_call("./rsync_script  .sh %s" %(str(path)))
        print(path + "will be copied to Norfile")
        subprocess.check_call("./s3_sync_script  .sh %s" %(str(path)))
        print(path + "will be copied to S3")
    else:
        print(path + "is not a valid bag.")
else:
    print(path + "is a file.") 



    
