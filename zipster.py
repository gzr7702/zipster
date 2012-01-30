import zipfile
import glob
import os
import sys
import getopt

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def main(argv=None):
    """A simple utility to zips all the files in a folder and names the zip file after that folder.
    It takes one argument: the path to the folder that you want to zip.
    """
    print("start")
    if argv is None:
        argv = sys.argv
        
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error as msg:
            raise Usage(msg)
    except Usage as err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2
    
    for opt in opts:
        if opt == 'h' or opt == 'help':
            Usage("zipster.py /path/to/folder")
            
    pth = args[0]

    new_path, fn_base = os.path.split(pth)
    fn = fn_base + ".zip"
    files_to_archive = glob.glob(os.path.join(fn_base, "*"))
    zf = zipfile.ZipFile(fn, "w", zipfile.ZIP_DEFLATED)
    for fn_to_archive in files_to_archive:
        if os.path.isfile(fn):
            zf.write(fn_to_archive)
    zf.close()
    return zf.filelist

if __name__ == "__main__":
    sys.exit(main())