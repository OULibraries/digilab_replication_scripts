import os
import bagit
import subprocess
import boto3
from pathlib import Path
import glob
import posixpath
import re

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
       buildBagList
       buildFileList
       uploadFileList

def buildDirectoryList(sourcePath):
#steps 1-3 from above
#get a list of bags from sourcePath--use glob or similar
        p = Path(sourcePath)
        allPaths = list(p.glob('**')) 
 
# select directories only
        rawPaths = str([i for i in allPaths if Path(i).is_dir()])
        dirPaths = []
        for i in allPaths:
           rawPaths=rawPaths.replace("('","*(")
           rawPaths=rawPaths.replace("')",")*")
           x = rawPaths.split("*")
           
           for i in x:
                if i.startswith("(") and i.endswith(")"):
                        dirPaths.append(i[1:-1])
           return dirPaths
        

        
# this function will return a list of valid bags only--tested        
def buildBagList(dirPaths):
# select valid bags from directories
        bagPaths = []
        for i in dirPaths:  
            bagPaths.append([i for i in dirPaths if bagit.Bag(i).is_valid()])
            return bagPaths
              
               
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