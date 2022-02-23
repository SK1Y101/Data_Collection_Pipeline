# fetch required modules
import boto3, os

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

def upload_to_aws(fileName, bucket, obj_Name=None):
    obj_Name = os.path.basename(fileName) if not obj_Name else obj_Name
    s3 = boto3.client("s3")
    with open(fileName, "rb") as f:
        s3.upload_fileobj(f, bucket, obj_Name)

def main():
    # fetch all the files to upload
    files = files_from_dir("source/raw_data")
    # show that to the user
    print("There are {} exoplanet files to upload".format(len(files)))

if __name__ == "__main__":
    main()