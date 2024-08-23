from pathlib import Path
import os
import glob
import boto3

from validate_and_sync_bags import validate_rsync_and_upload_to_s3


def main(bag_path, bucket, s3_dest, tag, rsync_dest):
    
        if not os.path.isdir(bag_path):
        print("%s is not a directory." % bag_path)
        return

        source_dir = os.path.split(bag_path("/"))
         #   find path up to Bagit/ and take dir after "/"
        
        dest_dir = os.path.join(rsync_dest, source_dir)

        s3_dest_dir = os.path.joint(bucket, source_dir)

# Now reassign bag_path, rsync_dest, and s3_dest with targeted directory values
        bag_path = source_dir

        rsync_dest = dest_dir

        s3_dest = s3_dest_dir

        validate_rsync_and_upload_to_s3(bag_path, bucket, s3_dest, tag, rsync_dest)
        
        #main function from validate_and_sync_bags.py

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bag_path", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--s3_dest", help="to which 'directory' in s3 bucket")
    parser.add_argument("--rsync_dest", help="local rsync dest")
    parser.add_argument("--tag", help="some tag to select files, like *png", default='*')
    args = parser.parse_args()
    main(bag_path=args.bag_path, bucket=args.bucket, s3_dest=args.s3_dest, tag=args.tag,
         rsync_dest=args.rsync_dest)