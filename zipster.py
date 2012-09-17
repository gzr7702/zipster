"""A simple utility that zips all the files in a folder and names the zip file after that folder.
It takes one argument: the path to the folder that you want to zip.
"""
import zipfile
import glob
import os
import argparse
import logging

def zipster(args):
    new_path, fn_base = os.path.split(args.source)
    print("base", fn_base)
    fn = fn_base + ".zip"
    files_to_archive = glob.glob(os.path.join(fn_base, "*"))
    zf = zipfile.ZipFile(fn, "w", zipfile.ZIP_DEFLATED)
    for fn_to_archive in files_to_archive:
        if os.path.isfile(fn):
            zf.write(fn_to_archive)
    zf.close()
    return zf.filelist

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zips all files in a directory and names the zip file after the directory")
    parser.add_argument("-s", "--source", metavar="P", help="The source directory that you would like zipped.")
    
    args = parser.parse_args()
    zipster(args)