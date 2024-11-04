import sys
import hashlib
import boto3
from pathlib import Path
from hmac import compare_digest

# These functions will need to be copied over and modified to return the values
# for data integrity validation. Print statements will also need to be changed
from findAndUploadBags import (
    buildDirectoryList,
    buildBagList,
    buildFileList,
    s3FileExists,
    norfileFileExists,
)


def buildDirectoryList(sourcePath):
    p = Path(sourcePath)
    # Non-recursive -- we only want one level of subdirectory from the sourcePath
    allPaths = list(p.glob("*"))
    # select top level objects and validate as a directory
    dirPaths = [str(i) for i in allPaths if i.is_dir()]
    print("%s will be tested for data integrity" % (dirPaths))
    return dirPaths


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


# 1. Check to see if bag exists in S3 and NAS
# 2. If exists, pull checksum from S3
def retrieveS3FileHash(fileName, bucket):  # return checksum in header call
    s3_client = boto3.client("s3")
    response = s3_client.get_object_attributes(
        Bucket=bucket, Key=fileName, ObjectAttributes=["ETag"]
    )
    return response


def retrieveNorfileBagManifest(fileName, syncDest):  # cat manifest and tagmanifest

    return manifestHash


# Checksums for every item are in manifest---.txt in bag
# Checksum for manifest---.txt, bagit.txt, and bag-info.txt are in tagmanifest---.txt
# The bag itself doesn't have a separate hash


# 3. Compare each key:value in dictionaries
def compareAndValidateMD5(s3FileHash, manifestHash):

    if s3FileHash == manifestHash:
        print("File integrity validated %s" % (fileName))

    else:
        print("Files are different")
        print("Hash from S3: %s" % (s3FileHash))
        print("Hash from NAS: %s" % (manifestHash))


# 6. Return result-- "success--tombstone bag %s" % ((fileName).relative_to(bagPath)), "failure--reupload bag"


def main(sourcePath, bucket, syncDest):

    dirPaths = buildDirectoryList(sourcePath)

    bagPaths = buildBagList(dirPaths)

    for bagPath in bagPaths:
        fileList = buildFileList(bagPath)
        compareAndValidateMD5(s3Hash, nasHash)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcePath", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--syncDest", help="local rsync dest")
    args = parser.parse_args()
    main(sourcePath=args.sourcePath, bucket=args.bucket, syncDest=args.syncDest)
