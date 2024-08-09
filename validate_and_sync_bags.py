#!/usr/bin/python

import bagit
import subprocess
import os
import boto3
import logging

from botocore.exceptions import ClientError
from config import *


def find_directories():
    if not os.path.isdir('path to object'):
        print("%s" + "is not a directory.")
        return
   
def validate_bag(bag_name): 
    bag_name = bagit.Bag('path to object')    
    if not bag_name.is_valid(): 
        print("%s" + "is not a valid bag.")
        return
    else:    
        subprocess.call(["rsync", "-avz", "--update", "--no-perms", "--omit-dir-times", "--logfile=$LOGFILE", "$MOUNTPOINT"])


#check if "file_name" can refer to a bag/directory 
def upload_to_s3(bag_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(bag_name)

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_to_s3(bag_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
    print(file_name + "uploaded to s3.")