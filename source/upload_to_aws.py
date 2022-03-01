# fetch required modules
from tqdm import trange
import boto3, os, uuid

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

def upload_to_aws(fileName, bucket, obj_Name=None, check_for_duplicate=True):
    obj_Name = os.path.basename(fileName) if not obj_Name else obj_Name
    s3 = boto3.client("s3")
    # check for duplicates if desired
    if check_for_duplicate:
        # if the object exists
        if obj_Name in [e['Key'] for p in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket) for e in p['Contents']]:
            # stop the function
            return False
    s3.upload_file(fileName, bucket, obj_Name)

# upload files to aws, keeping the directory structure
def multiupload(files, bucket, remove_dir):
    # fetch all the files already uploaded
    objs = [e['Key'] for p in boto3.client("s3").get_paginator("list_objects_v2").paginate(Bucket=bucket) for e in p['Contents']]
    # ensure we don't start with a file marker
    for x in trange(len(files)):
        file = files[x]
        fname = file.replace(remove_dir, "")
        # upload it if it's not already been uploaded
        if fname not in objs:
            upload_to_aws(file, bucket, fname, False)

def main():
    # fetch all the files to upload from within the data folder
    files = files_from_dir("source/raw_data")
    # show that to the user
    print("There are {} exoplanet files to upload".format(len(files)))
    # try uploading the files!
    multiupload(files, "exoplanet", "source/raw_data/")

if __name__ == "__main__":
    main()