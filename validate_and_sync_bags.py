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
from upload_to_s3 import upload_dir

#substitute variable bag_path for 'path to object' in functions
#use isdir in __main__
def validate_and_rsync(bag_path, bucket, s3_dest, tag, rsync_dest):
    
    s3_client = boto3.client('s3')

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
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


#if the bag is valid, pass the path to rsync
       
   
    subprocess.call(['rsync', '-av', '--dry-run', '--update', '--no-perms', '--omit-dir-times',"{0}".format(bag_path),"{0}".format(rsync_dest)])

    upload_dir(bag_path, bucket, s3_dest, tag)
#    upload_dir(bag_path=args.bag_path, bucket=args.bucket, s3_dest=args.s3_dest)
     
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bag_path", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--s3_dest", help="to which 'directory' in s3")
    parser.add_argument("--rsync_dest", help="local rsync dest")
    parser.add_argument("--tag", help="some tag to select files, like *png", default='*')
    args = parser.parse_args()

    validate_and_rsync(bag_path=args.bag_path, bucket=args.bucket, s3_dest=args.s3_dest, tag=args.tag, rsync_dest=args.rsync_dest)
