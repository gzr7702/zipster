import unittest
import os
import shutil
import zipfile
import zipster 

class TestCase(unittest.TestCase):
    def setUp(self):
        #change this to your test path
        self.path = "/Users/rob/Documents/workspace/zipster/zip_test"
        self.zipFilename = "zip_test.zip"
        os.mkdir(self.path)
        self.fNames = ["file1", "file2", "file3"]
        for fn in self.fNames:
            f = open(os.path.join(self.path, fn), "w")
            f.write("some data")
            f.close()
    
    def test_zipster(self):
        #add app name to args becuase that's what will happen from the command line.
        args = ["zipster.py", self.path]
        zipster.main(args)
        #change this to your test path
        self.newPath = "/Users/rob/Documents/workspace/zipster"
        #handle an unfound zip file gracefully.
        try:
            zf = zipfile.ZipFile(os.path.join(self.newPath, self.zipFilename), "r")
            files_in_archive = zf.namelist()
            zf.close()
            observed = set([os.path.basename(f) for f in files_in_archive])
            expected = set(self.fNames)
            self.assertEqual(observed, expected)
        except IOError as ioe:
            print(ioe, "Test failed because a zip file was never created.")
    
    def tearDown(self):
        os.remove(self.zipFilename)
        try:
            shutil.rmtree(self.path, ignore_errors=True)
        except IOError:
            pass