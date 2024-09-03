import os

from validate_and_sync_bags import validate_and_rsync


def main(bag_path, bag_name, bucket, s3_dest, tag, rsync_dest):
#"continue" statement to move to next iteration rather than return 
# for file in __    
    if not os.path.isdir(bag_path):
        print("%s is not a directory." % bag_path)
        return
          
    if os.path.isdir(bag_path):
        base_path = os.path.split(bag_path)[0]
        bag_name = os.path.split(bag_path)[1]
        s3_dest_dir = os.path.split(base_path)[1]
    else:
        raise Exception("{0} is not a valid bag path".format(bag_path))
    if "private" in base_path or "preservation" in base_path or "shareok" in base_path:
        s3_subdir = os.path.split(base_path)[1]
        s3_base_dir="private"
        s3_dest = os.path.join(s3_base_dir,s3_subdir)
        print(os.path.join(s3_private_path,s3_subdir,bag_name))
        validate_and_rsync(bag_path, bucket, s3_dest, tag, rsync_dest)
    else:
        s3_dest="source"
        print(s3_dest)
        validate_and_rsync(bag_path, bucket, s3_dest, tag, rsync_dest)
    

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
    main(bag_path=args.bag_path, bag_name=args.bag_name, bucket=args.bucket, s3_dest=args.s3_dest,
         tag=args.tag, rsync_dest=args.rsync_dest)