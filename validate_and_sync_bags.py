#!/usr/bin/python

import bagit
import subprocess
import os
import boto3
import logging
import sys
import glob


from botocore.exceptions import ClientError
#variables imported from config.py must be listed explicitly


#substitute variable bag_path for 'path to object' in functions
#use isdir in __main__
def main():
    bag_path = sys.argv[1]
    rsync_dest = sys.argv[2]
    bucket = sys.argv[3]
    s3_client = boto3.client('s3')

#    if not os.path.isdir(bag_path):
#        print("%s is not a directory." % bag_path)
#        return
    
 #   if not os.path.ismount(rsync_dest):
 #       print("%s is not a mounted share" % rsync_dest)
 #       return
    
#    try:
#        bag = bagit.Bag(bag_path)    
#        if not bag.is_valid(): 
#            print("%s is not a valid bag." % bag_path)
#            return
#    except Exception as err:
#        print(f"Unexpected {err=}, {type(err)=}")
#        raise


#if the bag is valid, pass the path to rsync
       
   
 #   subprocess.call(['rsync', '-av', '--dry-run', '--update', '--no-perms', '--omit-dir-times',"{0}".format(bag_path),"{0}".format(rsync_dest)])


    #iterate through bag and list files
#    files = glob.glob(bag_path)
#    for file in files:
#        try:
#            response = s3_client.upload_file(file, Bucket='ul-bagit-test', Key=bag_path+file)
#            print('uploaded ', file)
#        except Exception as err:
#            print(f"Unexpected {err=}, {type(err)=}")
#            raise
    try:
        response = s3_client.put_object(Body=bag_path, Bucket='ul-bagit-test', Key=bag_path)
        print('uploaded ', bag_path)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
     
if __name__ == "__main__":
    main()
