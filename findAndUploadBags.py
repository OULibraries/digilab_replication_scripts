from pathlib import Path
from subprocess import CalledProcessError

import datetime
import os
import subprocess
import boto3
import bagit

from botocore.exceptions import ClientError
from pprint import pprint


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
        test = bagit.Bag(path).is_valid()
        print("%s is a bag" % (path))
        return test
    except bagit.BagError as e:
        print("%s is not a bag" % (path))


def buildBagList(dirPaths):
    """Filter list of directories for bags."""

    # Limit for debugging
    # slicedDirPaths=dirPaths[0:2]
    # bagPaths = [i for i in slicedDirPaths if bagExceptionWrapper(i)]

    bagPaths = [i for i in dirPaths if bagExceptionWrapper(i)]
    print("%s are valid bags" % (str(bagPaths)))
    return bagPaths


def buildFileList(bagPath):
    """Create lists of direcotires that might be bags."""
    p = Path(bagPath)
    allPaths = p.glob("**/*")
    filePaths = [f for f in allPaths if not Path(f).is_dir()]
    return filePaths


# Needs review!!!!
def s3FileExists(fileName, bucket):
    """Check to see if path exists in S3"""
    s3_client = boto3.client("s3")
    try:
        s3_client.head_object(Bucket=bucket, Key=fileName)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        else:
            raise


def norfileFileExists(syncDest, pathInBag):
    """Check to see if path exists in norfile path"""
    p = Path("%s/%s" % (str(syncDest), str(pathInBag)))
    return p.exists()


def uploadFileList(sourcePath, fileList, bucket, syncDest, dryRun):
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
        if s3FileExists(str(bagAndSourceDir), bucket):
            print("Found s3://%s/%s, not uploading." % (bucket, bagAndSourceDir))
        elif dryRun:
            print("Dry run. Skipping upload to s3://%s/%s." % (bucket, bagAndSourceDir))
        else:
            s3_client.upload_file(fileName, bucket, str(bagAndSourceDir))
            print("Uploaded s3://%s/%s." % (bucket, bagAndSourceDir))

        # Skip files that we've already copied to norfile
        if norfileFileExists(syncDest, pathInBag):
            print("Found %s/%s, not copying." % (str(syncDest), str(pathInBag)))
        elif dryRun:
            print("Dry run. Skiping copy to %s/%s. " % (str(syncDest), str(pathInBag)))
        else:

            try:
                # We know this is a file because fileList is filtered for directories
                subprocess.check_call(
                    [
                        "./copyWithFullPath.sh",
                        str(p.name),
                        str(p),
                        str(pathInBag.parent),
                        syncDest,
                    ],
                )
                print(
                    "Copied %s/%s to norfile if not already present."
                    % (syncDest, str(pathInBag))
                )

            except CalledProcessError as e:
                print("Error while copying file.", e)


def main(sourcePath, bucket, syncDest, dryRun):
    """Search the given dir for bags and copy them to norfile and S3"""

    # TODO FIXME This doesn't work and needs replaced.
    # The syncDest is on a mounted share, but isn't the root of it anymore
    #   if not os.path.ismount(syncDest):
    #       print("%s is not a mounted share" % (syncDest))
    #       return None

    # Find the directories that might be bags at our sourcePath
    print("Building a list of potential bag dirs to process.")
    dirPaths = buildDirectoryList(sourcePath)
    # Filter out everything that doesn't look like a bag
    print("Filtering for valid bags.")
    bagPaths = buildBagList(dirPaths)

    for bagPath in bagPaths:

        print("START at %s" % (datetime.datetime.now()))
        print("Processing bag at %s\n" % (bagPath))
        fileList = buildFileList(bagPath)
        uploadFileList(sourcePath, fileList, bucket, syncDest, dryRun)
        print("END at %s" % (datetime.datetime.now()))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sourcePath", help="Source to process for bags", required="True"
    )
    parser.add_argument("--bucket", help="Destination bucket in aws", required="True")
    parser.add_argument("--syncDest", help="Destination path", required="True")

    parser.add_argument(
        "--dryRun", action="store_true", help="test, but don't make changes"
    )

    args = parser.parse_args()

    pprint(args)

    main(
        sourcePath=args.sourcePath,
        bucket=args.bucket,
        syncDest=args.syncDest,
        dryRun=args.dryRun,
    )
