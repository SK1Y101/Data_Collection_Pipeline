# fetch required modules
from time import sleep as wait
from tqdm import trange
import boto3, os, time

wdir = os.getcwd()

# fetch all files in a directory
def files_from_dir(folder):
    dirs = os.listdir(folder)
    # fetch the files
    files = [folder+"/"+x for x in dirs if os.path.isfile(folder+"/"+x)]
    # fetch the files in the folders
    folders = [files_from_dir(folder+"/"+x) for x in dirs if os.path.isdir(folder+"/"+x)]
    # and return both
    return flatten(files + folders)

# convert a nested list to a linear one
def flatten(lis):
    # fetch the non-nested
    out = [x for x in lis if not isinstance(x, list)]
    # fetch the nested
    out += [y for x in lis if isinstance(x, list) for y in flatten(x)]
    # and return
    return sorted(out)

def upload_to_aws(fileName, bucket, obj_Name=None, check_for_duplicate=True, awsFiles=None, stale_time=7):
    obj_Name = os.path.basename(fileName) if not obj_Name else obj_Name
    # check for duplicates if desired
    if check_for_duplicate:
        # get a list of files if not given
        if not awsFiles:
            awsFiles = getAwsFiles(bucket)
        # if the dosen't need to be (re)uploaded
        if awsNotStale(obj_Name, bucket, awsFiles, stale_time):
            # stop the function
            return False
    # upload
    s3 = boto3.client("s3")
    s3.upload_file(fileName, bucket, obj_Name)

# upload files to aws, keeping the directory structure
def multiupload(files, bucket, remove_dir, awsFiles=None, stale_time=7):
    if not awsFiles:
        awsFiles = getAwsFiles(bucket)
    # ensure we don't start with a file marker
    for x in trange(len(files)):
        file = files[x]
        fname = file.replace(remove_dir, "")
        upload_to_aws(file, bucket, fname, True, awsFiles, stale_time)

# check if a file a) exists and b) is not stale on aws. returns false if the file needs to be (re)uploaded
def awsNotStale(filename, bucket, awsFiles=None, stale_time=7):
    # get file reference
    if not awsFiles:
        awsFiles = getAwsFiles(bucket)
    # decompose references
    fnames, fdetails = awsFiles
    # if the file dosen't exist
    if filename not in fnames:
        return False
    # fetch modification time
    fidx = fnames.index(filename)
    thisfile = fdetails[fidx]
    mtime = thisfile["LastModified"]
    # check if it's larger than our stale time
    if (time.time() - mtime.timestamp()) > stale_time*86400:
        return False
    # otherwise, the file exists, and is not stale
    return True

# fetch all files in the s3 bucket
def getAwsFiles(bucket):
    # start client
    s3 = boto3.client("s3")
    # get files
    files = [e for p in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket) for e in p["Contents"]]
    # get filenames
    fileKeys = [file["Key"] for file in files]
    # return
    return fileKeys, files

def main():
    # fetch all the files to upload from within the data folder
    files = files_from_dir("source/raw_data")
    # show that to the user
    print("There are {} exoplanet files to upload".format(len(files)))
    # try uploading the files!
    multiupload(files, "exoplanet", "source/raw_data/")

if __name__ == "__main__":
    main()