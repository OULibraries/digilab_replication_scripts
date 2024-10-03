import os
import bagit
import subprocess
import boto3
from pathlib import Path
import glob

from botocore.exceptions import ClientError
from subprocess import CalledProcessError


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


def s3FileExists(fileName, bucket):
    s3_client = boto3.client("s3")
    try:
        s3_client.head_object(Bucket=bucket, Key=fileName)
        print("EXISTS: %s found in %s" % (fileName, bucket))
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("404: %s not found in %s" % (fileName, bucket))
        else:
            print("An unexpected error has occured")
        return False


# need to strip the first element from the path to create a valid path for rsync
def norfileFileExists(fileName, syncDest):
    delim = "/"
    sourceElements = Path(fileName).parts[1:]
    fileElements = "".join([str(elements) + delim for elements in sourceElements])
    p = Path("%s/%s" % (syncDest, fileElements))
    #    print("The path is %s and file name is %s" % (p, sourceElements[-1]))
    return p.exists()


def uploadFileList(fileList, bucket, syncDest):
    s3_client = boto3.client("s3")
    # check for files in s3--if they exist, exclude from upload
    # make sure to give the fileName as a string for boto3--it doesn't like Path objects as S3 Keys
    for fileName in fileList:
        if s3FileExists(str(fileName), bucket) is False:
            s3_client.upload_file(fileName, bucket, str(fileName))
            print("Uploaded file %s to %s" % (fileName, bucket))

        if norfileFileExists(fileName, syncDest) is False:
            try:
                delim = "/"
                sourceElements = Path(fileName).parts[0:2]
                syncBag = "".join(
                    [str(elements) + delim for elements in sourceElements]
                )
                syncBag = syncBag[: len(syncBag) - len(delim)]
                print("bag is %s" % (syncBag))

                subprocess.check_call(
                    [
                        "/home/mmalahy/syncCron.sh",
                        syncBag,
                        syncDest,
                    ]
                )
                print("%s is copied to %s" % (syncBag, syncDest))

            except CalledProcessError as e:
                print("an error has occured %s" % e)


def main(sourcePath, bucket, syncDest):
    """1)make a list of things that might be bags(in either private or source)--just top-level directories
    2)filter non-directories
    3)filter non-bags
    4)for each bag, build file list and upload files--s3 first
    """

    #    if not os.path.ismount(syncDest):
    #        print("%s is not a mounted share" % (syncDest))
    #        return

    dirPaths = buildDirectoryList(sourcePath)

    bagPaths = buildBagList(dirPaths)

    for bagPath in bagPaths:
        fileList = buildFileList(bagPath)
        uploadFileList(fileList, bucket, syncDest)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcePath", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--syncDest", help="local rsync dest")
    args = parser.parse_args()
    main(sourcePath=args.sourcePath, bucket=args.bucket, syncDest=args.syncDest)
