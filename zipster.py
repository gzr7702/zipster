#!/usr/bin/env python

"""
A simple utility that zips all the files in a folder and names the zip file after that folder.
It takes one argument: the path to the folder that you want to zip.
"""
import zipfile
import glob
import os
import argparse
import logging
import shutil

def zipster(args):
    new_path, fn_base = os.path.split(args.source)

    if not os.path.exists(args.source):
        print("Directory %s does not exist" % fn_base)
        logging.error("Directory %s does not exist" % fn_base)
        exit(1)

    logging.info("Zipping file " + fn_base)
    fn = fn_base + ".zip"
    files_to_archive = glob.glob(os.path.join(fn_base, "*"))
    zf = zipfile.ZipFile(fn, "w", zipfile.ZIP_DEFLATED)
    
    for fn_to_archive in files_to_archive:
        logging.info("Adding file " + fn_to_archive + " to archive " + fn_base)
        if os.path.isfile(fn):
            zf.write(fn_to_archive)
    zf.close()
            
    if args.dest:
        if not os.path.exists(args.dest):
            print("Directory %s does not exist. Leaving zip file where it is." % fn_base)
            logging.error("Directory %s does not exist. Leaving zip fle where it is." % fn_base)
        else:
            dest = os.path.join(args.dest, fn)
            logging.info("moving file " + fn + " to " + dest)
            shutil.move(fn, dest)
        
    logging.info("Done!")
    
    return zf.filelist

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zips all files in a directory and names the zip file after the directory")
    parser.add_argument("-s", "--source", metavar="source", required=True,
                        help="The source directory that you would like zipped.")
    parser.add_argument("-d", "--dest", metavar="destination", help="If specified, a destination directory that the zip file will be moved to.")

    args = parser.parse_args()
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
    logging.basicConfig(filename="zipsterlog.txt", level=logging.INFO, format=LOG_FORMAT)
    zipster(args)
