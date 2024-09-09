#pseudocode logic working file for filesync script
import os
import bagit
import subprocess
import boto3
from pathlib import Path
import glob

from botocore.exceptions import ClientError
'''bag_path   == the path to the directory to look for bags e.g. ~/Bagit/source/
   bucket     == the name of the bucket in s3
   key        == the full key in s3 is bucket+path-to-destination e.g. ul-bagit-test/source/
   tag        == default is null, not currently in use but can be added
   rsync_dest == destination directory on Norfile for rsync from NASes
'''
def main(bag_path, bucket, key, tag, rsync_dest):
        
        s3_client = boto3.client('s3')
        
        #verify that rsync_dest in norfile is mounted
        if not os.path.ismount(rsync_dest):
                print("%s is not a mounted share" % rsync_dest)
                return
        #take path to NAS directory
        #Iterate through skipping tombstones and files, verifying directories
        for dirs in os.listdir(bag_path):
                for dirname in dirs:
                        outPath = os.path.join(bag_path,'/',dirname)
                        print(outPath)
                        if not os.path.isdir(dirname):
                                print("%s is not a directory." % dirname)
                                continue

        #Find directories and send to method determining if it is a bag    
                        try:
                                bag = bagit.Bag(dirname)    
                                if not bag.is_valid(): 
                                        print("%s is not a valid bag." % dirname)
                                        continue
        #If not a bag continue loop
                        except Exception as err:
                                print(f"Unexpected {err=}, {type(err)=}")
                                raise

        #If is bag determine rsync and s3 directory
        # need to set s3_dest directory for rsync dest = nas path + rsync_dest
                        if "private" in dirname or "preservation" in dirname or "shareok" in dirname:
                                dest_subdir = os.path.split(dirname)[1]
                                rsync_dest = os.path.join("private",dest_subdir)
                                key = os.path.join(bucket,rsync_dest)
                                print(os.path.join("private",dest_subdir))
                                subprocess.call(['rsync', '-av', '--dry-run', '--update', '--no-perms', '--omit-dir-times',"{0}".format(bag_path),"{0}".format(rsync_dest)])
                                upload_dir(bag_path, bucket, key, tag, prefix='/')
                        else:
                                rsync_dest="source"
                                key = os.path.join(bucket,rsync_dest)
                                print(rsync_dest)
                                subprocess.call(['rsync', '-av', '--dry-run', '--update', '--no-perms', '--omit-dir-times',"{0}".format(bag_path),"{0}".format(rsync_dest)])
                                upload_dir(bag_path, bucket, key, tag, prefix='/')


        
#validate_and_rsync(bag_path, bucket, key ((this should be Key)), rsync_dest)
#invoke validate_and_rsync
        '''rsync to norfile with destination folder matching source in NAS then
        invoke upload_dir to upload to s3 in either source/ or private/
        # this script should use an argument for s3 Key rather than bucket to allow a path-like
        # key to be passed such as ul-bagit-test/private/preservation/a_bag'''
def upload_dir(bag_path, bucket, key, tag, prefix='/'):
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
                        if fileName.startswith(prefix):
                        # only modify the text if it starts with the prefix
                                fileName = fileName.replace(prefix, "", 1) # remove one instance of prefix
                        print(f"fileName {fileName}")

        awsPath = os.path.join(key, str(fileName))
        s3.meta.client.upload_file(fileName, bucket, awsPath)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--bag_path", help="which dir to upload to aws")
    parser.add_argument("--bucket", help="to which bucket to upload in aws")
    parser.add_argument("--key", help="s3 key (path) to which 'directory' in s3 bucket")
    parser.add_argument("--rsync_dest", help="local rsync dest")
#    parser.add_argument("--bag_name", help="name of the bag_name to copy")
    parser.add_argument("--tag", help="some tag to select files, like *png", default='*')
    args = parser.parse_args()
    main(bag_path=args.bag_path, bucket=args.bucket, key=args.key,
         tag=args.tag, rsync_dest=args.rsync_dest)