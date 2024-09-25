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
        print("%s is not a mounted share" % (rsyncDest))
        return

    dirPaths = buildDirectoryList(sourcePath)

    bagPaths = buildBagList(dirPaths)

    for bagPath in bagPaths:
        fileList = buildFileList(bagPath)
        uploadFileList(fileList, bucket, rsyncDest)


def buildDirectoryList(sourcePath):
    p = Path(sourcePath)
    # Non-recursive -- we only want one level of subdirectory from the sourcePath
    allPaths = list(p.glob("*"))
    # select top level objects and validate as a directory
    dirPaths = [str(i) for i in allPaths if i.is_dir()]
    print("%s will be validated as bags" % (dirPaths))
    return dirPaths


## Need to append valid bag to list--the function stops after the first bag tested
def bagExceptionWrapper(path):
    try:
        return bagit.Bag(path).is_valid()
    except bagit.BagError as e:
        print("%s is not a bag" % (path))


# this function selects valid bags from directories
def buildBagList(dirPaths):
    bagPaths = [i for i in dirPaths if bagExceptionWrapper(i)]
    print("%s are valid bags" % (str(bagPaths)))
    return bagPaths


def buildFileList(bagPath):
    p = Path(bagPath)
    allPaths = p.glob("**/*")
    filePaths = [f for f in allPaths if not Path(f).is_dir()]
    return filePaths


def uploadFileList(fileList, bucket, rsyncDest):
    s3_client = boto3.client("s3")
    # check for files in s3--if they exist, exclude from upload

    for fileName in fileList:
        if not s3FileExists(fileName, bucket):
            s3_client.upload_file(fileName, bucket, str(fileName))
            print("Uploaded file: %s" % (fileName))

        if not norfileFileExists(fileName, rsyncDest):
            subprocess.call(
                [
                    "rsync",
                    "-av",
                    "--dry-run",
                    "--ignore-existing",
                    "--no-perms",
                    "--omit-dir-times",
                    "{0}".format(fileName),
                    "{0}".format(rsyncDest),
                ]
            )
            print("Copied file %s to %s" % (fileName, rsyncDest))


def s3FileExists(fileName, bucket):
    s3_client = boto3.client("s3")
    try:
        s3_client.head_object(Bucket=bucket, Key=fileName)
        return True
    except:
        return False


def norfileFileExists(fileName, rsyncDest):
    p = Path("%s, %s" % (rsyncDest, fileName))
    return p.exists()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcePath", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--rsyncDest", help="local rsync dest")
    args = parser.parse_args()
    main(sourcePath=args.sourcePath, bucket=args.bucket, rsyncDest=args.rsyncDest)
