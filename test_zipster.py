import unittest
import os
import shutil
import zipfile
import zipster 
import subprocess

class TestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = "zip_test"
        self.zip_filename = "zip_test.zip"
        os.mkdir(self.test_dir)
        self.file_names = ["file1", "file2", "file3"]
        for fn in self.file_names:
            f = open(os.path.join(self.test_dir, fn), "w")
            f.write("some data")
            f.close()
    
    def test_zipster(self):
        #call zipster with arg to dir that should be zipped
        #obviously, you need to change this to the path on your system or system wide python
        command = ["/usr/local/bin/python3", "zipster.py", "-s", "zip_test"]
        subprocess.call(command)
        #handle an unfound zip file gracefully.
        files_in_archive = None
        observed = None
        try:
            zf = zipfile.ZipFile(self.zip_filename, "r")
            files_in_archive = zf.namelist()
            zf.close()
            observed = set([os.path.basename(f) for f in files_in_archive])
        except IOError as ioe:
            print(ioe)
        expected = set(self.file_names)
        self.assertEqual(observed, expected)
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        if os.path.exists(self.zip_filename):
            os.remove(self.zip_filename)
        else:
            print("Zip file must not have been created.")