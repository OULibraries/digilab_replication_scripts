from pathlib import Path
import os
import glob
import boto3

from validate_and_sync_bags import validate_and_rsync


def main(bag_path, bag_name, bucket, s3_dest, tag, rsync_dest):
    
    if not os.path.isdir(bag_path):
        print("%s is not a directory." % bag_path)
        return
        


def locate_bag(bag_path):
           
    if os.path.isdir(bag_path):
        base_path = os.path.split(bag_path)[0]
        bag_name = os.path.split(bag_path)[1]
        s3_dest = os.path.split(base_path)[1]
    else:
        raise Exception("{0} is not a valid bag path".format(bag_path))
    if "private" in base_path or "preservation" in base_path or "shareok" in base_path:
        s3_subdir = os.path.split(base_path)[1]
        s3_base_dir="private"
        s3_private_path = os.path.join(s3_base_dir,s3_subdir,bag_name)
        return os.path.join(s3_private_path,bag_name)
    else:
        s3_base_dir="source"
        return os.path.join(s3_base_dir,bag_name),s3_base_dir

     #   source_dir = os.path.split(bag_path("/"))
         #   find path up to Bagit/ and take dir after "/"
        
     #   dest_dir = os.path.join(rsync_dest, source_dir)

     #   s3_base_dir = os.path.joint(bucket, source_dir)

# Now reassign bag_path, rsync_dest, and s3_dest with targeted directory values
    bag_path = source_dir

    rsync_dest = dest_dir

    s3_dest = s3_base_dir

    validate_rsync_and_upload_to_s3(bag_path, bucket, s3_dest, tag, rsync_dest)
        
        #main function from validate_and_sync_bags.py

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bag_path", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--s3_dest", help="to which 'directory' in s3 bucket")
    parser.add_argument("--rsync_dest", help="local rsync dest")
    parser.add_argument("--bag_name", help="name of the bag_name to copy")
    parser.add_argument("--tag", help="some tag to select files, like *png", default='*')
    args = parser.parse_args()
    main(bag_path=args.bag_path, bag_name=args.bag_name, bucket=args.bucket, s3_dest=args.s3_dest, tag=args.tag,
         rsync_dest=args.rsync_dest)