import hashlib
from pathlib import Path
import logging
import bagit
import boto3
from botocore.exceptions import ClientError

# These functions will need to be copied over and modified to return the values
# for data integrity validation. Print statements will also need to be changed


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
    except bagit.BagError:
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
            print("404: %s not found in %s" % (fileName, bucket))
        else:
            print("An unexpected error has occured")
        return False

    # From oulibq tasks.py
    # def validate_s3_files(bag_name,local_source_path,s3_bucket,s3_base_key='source'):
    """
    Validate s3 files using the ETag 
    args:
        fileList, sourcePath, bucket
    """


def validateS3Hash(fileList, sourcePath, bucket):  # return manifest items to validate
    s3_client = boto3.client("s3")
    # open the manifest-md5.txt, parse the contents into filename and hash lists
    for fileName in fileList:
        p = Path(fileName)
        bagName = (p.parent).relative_to(sourcePath).parts[0]
        if s3FileExists(str(fileName, bucket)) is True:
            manifest = str("%s/manifest-md5.txt" % (bagName))
            manifestItems = []
            with open(manifest, "r") as f:
                for line in f.readlines():
                    lineSplit = iter(line.split(" "))
                    hashVal, manifestFilename = next(lineSplit), list(lineSplit)
                    manifestFilename = " ".join(manifestFilename).strip()
                    manifestItems.append({"md5": hashVal, "filename": manifestFilename})
            # format lists of hash and metadata for return after validation
            result = {}
            result["bucket"] = bucket
            result["verified"] = []
            result["error"] = []
            result["valid"] = [False]
            for row in manifestItems:
                md5, manifestFilename = row["md5"], row["manifestFilename"]
                try:
                    etag = s3_client.head_object(Bucket=bucket, Key=fileName)["ETag"][
                        1:-1
                    ]
                except ClientError:
                    errormsg = str(
                        "Failed to get S3 object hash for key: %s" % (fileName)
                    )
                    logging.error(errormsg)
                    raise ClientError(errormsg)
                if calculateMultipartETag(sourcePath, etag) or etag == md5:
                    result["verified"].append(fileName)
                else:
                    result["error"].append(fileName)
            if len(result["error"]) == 0:
                result["valid"] = True
        else:
            print("%s not found in %s" % (fileName, bucket))

        print("Status: Success: %s" % (fileName))
        return result["verified"]


def calculateMultipartETag(fileName, etag, chunkSizeMB=8):
    """
    calculates a multipart upload etag for amazon s3
    Arguments:
        fileName -- The file to calculate the etag
        etag -- s3 etag to compare
    Keyword Arguments:
        chunkSize -- The chunk size to calculate for.
    """

    md5s = []
    etagParts = etag.split("-")
    numParts = etagParts[1] if len(etagParts) > 1 else None
    chunkSize = chunkSizeMB * 1024**2
    with open(fileName, "rb") as fp:
        while True:
            data = fp.read(chunkSize)
            if not data:
                break
            md5s.append(hashlib.md5(data))

        if not md5s:
            return False

    # if hash of first chunk matches etag and
    # etag does not list number of chunks
    if md5s[0].hexdigest() == etag and not numParts:
        return True

    digests = b"".join(m.digest() for m in md5s)
    newMd5 = hashlib.md5(digests)
    newEtag = "%s-%s" % (newMd5.hexdigest(), len(md5s))
    if etag == newEtag:
        return True


def main(sourcePath, bucket):

    dirPaths = buildDirectoryList(sourcePath)

    bagPaths = buildBagList(dirPaths)

    for bagPath in bagPaths:
        fileList = buildFileList(bagPath)
        validateS3Hash(fileList, sourcePath, bucket)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--sourcePath", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    args = parser.parse_args()
    main(sourcePath=args.sourcePath, bucket=args.bucket)
