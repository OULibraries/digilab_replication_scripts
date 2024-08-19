#!/usr/bin/python

import bagit
import subprocess
import os
import boto3
import logging
import sys
import glob

#from secrets.py import ACCESS_KEY_ID,SECRET_ACCESS_KEY,REGION,BUCKET_NAME 
from botocore.exceptions import ClientError
#variables imported from config.py must be listed explicitly
#from config.py import 

#substitute variable bag_path for 'path to object' in functions
#use isdir in __main__
def main():
    bag_path = sys.argv[1]
    rsync_dest = sys.argv[2]
    bucket = sys.argv[3]
    s3_client = boto3.client('s3')

    if not os.path.isdir(bag_path):
        print("%s is not a directory." % bag_path)
        return
    
 #   if not os.path.ismount(rsync_dest):
 #       print("%s is not a mounted share" % rsync_dest)
 #       return
    
    try:
        bag = bagit.Bag(bag_path)    
        if not bag.is_valid(): 
            print("%s is not a valid bag." % bag_path)
            return
    except:
        print("not a bag")  


#if the bag is valid, pass the path to rsync

#keep -v for testing but don't need in prod
          
   
    subprocess.call(['rsync', '-av', '--dry-run', '--update', '--no-perms', '--omit-dir-times',"{0}".format(bag_path),"{0}".format(rsync_dest)])

    #iterate through bag and list files
    files = glob.glob(bag_path)
    files
    #upload contents of the bag
    for file in files:
        upload_to_s3(file, 'ul-bagit')
        print('uploaded ', file)



#There is no '--dryrun' arg in boto3
def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_to_s3(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    print(response)



if __name__ == "__main__":
    main()
