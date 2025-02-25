from pathlib import Path
from subprocess import CalledProcessError

import os
import subprocess
import boto3
import bagit

from botocore.exceptions import ClientError


def buildDirectoryList(sourcePath):
    """Make a list of directires in the sourcePath."""

    p = Path(sourcePath)
    # Non-recursive -- we only want one level of subdirectory from the sourcePath
    allPaths = list(p.glob("*"))
    # select top level objects and validate as a directory
    dirPaths = [str(i) for i in allPaths if i.is_dir()]
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
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("File %s/%s not found, will sync." % (bucket, fileName))
        else:
            print("An unexpected error has occured")
        return False


# removes top level source directory name to prevent duplicate directories in destination
def norfileFileExists(fileName, syncDest):
    # delim = "/"
    # sourceElements = Path(fileName).parts[1:]
    # fileElements = "".join([str(elements) + delim for elements in sourceElements])

    p = Path("%s/%s" % (syncDest, fileName))
    return p.exists()


def uploadFileList(sourcePath, fileList, bucket, syncDest):
    """Upload a list of files to specified locations in S3 and norfile"""

    s3_client = boto3.client("s3")

    for fileName in fileList:
        p = Path(fileName)
        sourceDir = Path(sourcePath).name
        pathInBag = p.relative_to(sourcePath)
        # use this version of the variable for private, preservation, and shareok directories

        # TODO find a better name for bagAndSourceDir
        # This is the filepath with both the bag name and the containing dir included.
        # Also, this is probably more complicated than it needs to be.
        bagAndSourceDir = Path("%s/%s" % (sourceDir, pathInBag))

        # Skip files that we've already uploaded to S3
        # TODO Right now we just check name, but should check hash
        # Casting to str because boto3 it doesn't like Path objects as S3 Keys
        if s3FileExists(str(bagAndSourceDir), bucket) is False:
            s3_client.upload_file(fileName, bucket, str(bagAndSourceDir))
            print("Uploaded %s/%s" % (bucket, bagAndSourceDir))
        else:
            print("Found %s/%s, not uploading." % (bucket, bagAndSourceDir))

        # Skip files that we've already copied to norfile
        if norfileFileExists(bagAndSourceDir, syncDest) is False:

            try:
                # We know this is a file because fileList is filtered for directories
                subprocess.check_call(
                    [
                        "./copyWithFullPath.sh",
                        str(p.name),
                        str(p),
                        str(pathInBag.parent ),
                        syncDest,
                    ],
                )
                print(
                    "Added %s/%s to norfile if not already present."
                    % (syncDest, str(pathInBag))
                )

            except CalledProcessError as e:
                print("An error has occurred", e)


def main(sourcePath, bucket, syncDest):
    """Search the given dir for bags and copy them to norfile and S3"""

    # TODO FIXME This doesn't work and needs replaced.
    # The syncDest is on a mounted share, but isn't the root of it anymore
    #   if not os.path.ismount(syncDest):
    #       print("%s is not a mounted share" % (syncDest))
    #       return None

    # Find the directories that might be bags at our sourcePath
    dirPaths = buildDirectoryList(sourcePath)
    # Filter out everything that doesn't look like a bag
    bagPaths = buildBagList(dirPaths)

    for bagPath in bagPaths:

        print("START")
        print("Processing bag at %s\n" % (bagPath))

        fileList = buildFileList(bagPath)
        uploadFileList(sourcePath, fileList, bucket, syncDest)

        print("END")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcePath", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--syncDest", help="local rsync dest")
    args = parser.parse_args()
    main(sourcePath=args.sourcePath, bucket=args.bucket, syncDest=args.syncDest)
