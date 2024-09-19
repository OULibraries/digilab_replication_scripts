import os
import bagit
import subprocess
import boto3
from pathlib import Path
import glob

from botocore.exceptions import ClientError


def main(sourcePath, bucket, rsyncDest):
    """1)make a list of things that might be bags(in either private or source)--just top-level directories
    2)filter non-directories
    3)filter non-bags
    4)for each bag, build file list and upload files--s3 first
    """

    if not os.path.ismount(rsyncDest):
        print("%s is not a mounted share" % rsyncDest)
        return

    dirPaths = buildDirectoryList(sourcePath)

    bagPaths = buildBagList(dirPaths)

    for bagPath in bagPaths:
        fileList = buildFileList(bagPath)
        uploadFileList(fileList, bucket)


def buildDirectoryList(sourcePath):
    p = Path(sourcePath)
    # Non-recursive -- we only want one level of subdirectory from the sourcePath
    allPaths = list(p.glob("*"))
    # select top level objects and validate as a directory
    dirPaths = [str(i) for i in allPaths if i.is_dir()]
    return dirPaths


# ADD print statement dirPaths, "to be validated for rsync and upload to s3"


def bagExceptionWrapper(path):
    try:
        return bagit.Bag(path).is_valid()
    except bagit.BagError as e:
        print("%s is not a bag" % (path))


# this function selects valid bags from directories
def buildBagList(dirPaths):
    bagPaths = [i for i in dirPaths if bagExceptionWrapper(i)]
    return bagPaths


# ADD print statement of bagPaths, "will be rsynced and uploaded to s3"


def buildFileList(bagPath):
    p = Path(bagPath)
    allPaths = p.glob("**/*")
    filePaths = [f for f in allPaths if not Path(f).is_dir()]
    return filePaths


def uploadFileList(fileList, bucket):
    s3_client = boto3.client("s3")

    for fileName in fileList:
        s3_client.upload_file(fileName, bucket, str(fileName))


# ADD print statement reporting bags uploaded successfully

# ADD rsync command string

# TODO--New features:

# add guardrail to prevent overwriting objects in s3--see https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html --may not work for our use case
# could do s3 ls on the bucket and if bag == bag from s3 skip it

# either include arguments in upload_file to compute checksum or
# add function like def checksumBags()

# NOTE: *If we change upload_file to put_object we can use the --if-none-match kwarg to prevent
# overwrites. This also allows us to use the checksum functionality built into the s3 PutObject api* https://docs.aws.amazon.com/AmazonS3/latest/API/API_PutObject.html#API_PutObject_Examples

# Does this negate the need to list the files individually? --We probably still want to know exactly # what is being uploaded and some of the files are very large so uploading a bag at a time might be a
# risky

# Bags contain 2 manifest files and 2 tagmanifest files--manifest contains checksums
# for the Data/ directory and each object contained within. Tagmanifest contains
# checksums for bagit.txt, bag-info.txt, and the 2 manifest files. We could checksum the
# the bag on upload and it would contain the nested checksums already within
# NOTE: manifest and tagmanifest checksums are hex and would need to be converted to
#       base64 for use with s3 if we opted for "precalculated checksum"

# don't upload if checksums don't match, print list of those bags

# print list of items with matching checksums


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcePath", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--rsyncDest", help="local rsync dest")
    args = parser.parse_args()
    main(sourcePath=args.sourcePath, bucket=args.bucket, rsyncDest=args.rsyncDest)
