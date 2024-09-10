import os
import bagit
import subprocess
import boto3
from pathlib import Path
import glob

from botocore.exceptions import ClientError

def main(sourcePath, bucket, rsyncDest):
       
       '''1)make a list of things that might be bags(in either private or source)--just top-level directories
          2)filter non-directories
          3)filter non-bags
          4)for each bag, build file list and upload files--s3 first
       '''

       if not os.path.ismount(rsyncDest):
            print("%s is not a mounted share" % rsyncDest)
            return
       
       buildDirectoryList
       buildFileList
       uploadFileList

def buildDirectoryList(sourcePath):
       #steps 1-3 from above
#get a list of bags from sourcePath--use glob or similar
        p = Path(sourcePath)
        allPaths = p.glob('**')
        for i in allPaths:
            bagName = [i for i in allPaths if Path(i).is_dir()]
            print("bagName", bagName)    
#Find directories and send to method determining if it is a bag -- build bag list

#PosixPath from allPaths output above not accepted as arg for bag=bagit.Bag(name)--unsuccessful in casting to string or otherwise slicing list
            for name in bagName:
                bag = bagit.Bag(name)   #error here 
                if not bag.is_valid(): 
                    print("%s is not a valid bag." % name)
                        
                else:
                    validBags = [name for name in allPaths if bagit.Bag(bagName).is_valid()]
                print("validBags", validBags)               
    #return list of valid bags
                return validBags
               
def buildFileList(validBags):
        p = Path(validBags)
        allPaths = p.glob('**/*')
        filePaths = [f for f in allPaths if not Path(f).is_dir()]
        return filePaths
        

def uploadFileList(fileList, bucket):
        s3_client = boto3.client('s3')

        for fileName in fileList:             
            s3_client.upload_file(fileName, bucket, str(fileName))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcePath", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--rsyncDest", help="local rsync dest")
    args = parser.parse_args()
    main(sourcePath=args.sourcePath, bucket=args.bucket, rsyncDest=args.rsyncDest)