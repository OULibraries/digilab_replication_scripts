#!/usr/bin/python

import bagit
import subprocess
import os
import boto3
import logging
import sys

from botocore.exceptions import ClientError
#from config import *

#substitute variable bag_path for 'path to object' in functions
#use isdir in __main__
def main():
    bag_path = sys.argv[1]
    rsync_dest = sys.argv[2]
    bucket = sys.argv[3]

    if not os.path.isdir(bag_path):
        print("%s is not a directory." % bag_path)
        return
    
    if not os.path.ismount(rsync_dest):
        print("%s is not a mounted share" % rsync_dest)
        return
    
    try:
        bag = bagit.Bag(bag_path)    
        if not bag.is_valid(): 
            print("%s is not a valid bag." % bag_path)
            return
    except:
        print("not a bag")  


#if the bag is valid, pass the path to rsync--not sure the best way to do this

#keep -v for testing but don't need in prod
# pull in variable values from config then --dry-run            
#    subprocess.call(['rsync -av --dry-run --update --no-perms --omit-dir-times $bag_path $rsync_dest'], shell=True)
    
    subprocess.call(['rsync', '-av', '--dry-run', '--update', '--no-perms', '--omit-dir-times',"{0}".format(bag_path),"{0}".format(rsync_dest)],shell=True)

#check if "file_name" can refer to a bag/directory

bag_path = "./test_valid_bag"
bucket = "s3://ul-bagit/source/"
def upload_to_s3(bag_path, bucket, object_name=None, ExtraArgs={'dryrun'}):
    if object_name is None:
        object_name = os.path.basename(bag_path)

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_to_s3(bag_path, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    print(bag_path, bucket, object_name)

#put communication inside __main__
#    print(file_name + "uploaded to s3.")
if __name__ == "__main__":
    main()
