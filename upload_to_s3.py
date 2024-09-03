""" upload one directory from the current working directory to aws """
from pathlib import Path
import os
import glob
import boto3

def upload_dir(bag_path, bucket, key, tag, prefix='/'):
    """
    from current working directory, upload a 'bag_path' with all its subcontents (files and subdirectories...)
    to a aws bucket
    Parameters
    ----------
    bag_path :   localDirectory to be uploaded, with respect to current working directory
    s3_dest : prefix 'directory' in aws
    bucket : bucket in aws
    tag :        tag to select files, like *png
                 NOTE: if you use tag it must be given like --tag '*txt', in some quotation marks... for argparse
    prefix :     to remove initial '/' from file names

    Returns
    -------
    None
    """
    s3 = boto3.resource('s3')
    cwd = str(Path.cwd())
    p = Path(os.path.join(Path.cwd(), bag_path))
    mydirs = list(p.glob('**'))
    for mydir in mydirs:
        fileNames = glob.glob(os.path.join(mydir, tag))
        fileNames = [f for f in fileNames if not Path(f).is_dir()]
        rows = len(fileNames)
        for i, fileName in enumerate(fileNames):
            fileName = str(fileName).replace(cwd, '')
            if fileName.startswith(prefix):  # only modify the text if it starts with the prefix
                fileName = fileName.replace(prefix, "", 1) # remove one instance of prefix
            print(f"fileName {fileName}")

            awsPath = os.path.join(key, str(fileName))
            s3.meta.client.upload_file(fileName, bucket, awsPath)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bag_path", help="which local dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--s3_dest", help="to which 'directory' in aws")
    parser.add_argument("--tag", help="some tag to select files, like *png", default='*')
    args = parser.parse_args()

    upload_dir(bag_path=args.bag_path, bucket=args.bucket,
               s3_dest=args.s3_dest, tag=args.tag)