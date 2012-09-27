import unittest
import os
import shutil
import zipfile
import zipster 
import subprocess

class TestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = "zip_test"
        self.archive_dir = "archive"
        self.zip_filename = "zip_test.zip"
        os.mkdir(self.test_dir)
        os.mkdir(self.archive_dir)
        self.file_names = ["file1", "file2", "file3"]
        for fn in self.file_names:
            f = open(os.path.join(self.test_dir, fn), "w")
            f.write("some data")
            f.close()
            
    def test_zipster(self):
        "Test basic functionality"
        #call zipster with arg to dir that should be zipped
        #obviously, you need to change this to the path on your system or system wide python
        command = ["/usr/local/bin/python3", "zipster.py", "-s", "zip_test"]
        subprocess.call(command)
        files_in_archive = None
        observed = None
        #handle an unfound zip file gracefully.
        try:
            zf = zipfile.ZipFile(self.zip_filename, "r")
            files_in_archive = zf.namelist()
            zf.close()
            observed = set([os.path.basename(f) for f in files_in_archive])
        except IOError as ioe:
            print(ioe)
        expected = set(self.file_names)
        self.assertEqual(observed, expected)
        
    def test_archive(self):
        "Test functionality where zip file is moved to archive folder"
        #call zipster with arg to dir that should be zipped and arg to dir that where zip file will be stored
        #obviously, you need to change this to the path on your system or system wide python
        command = ["/usr/local/bin/python3", "zipster.py", "-s", "zip_test", "-d", "archive"]
        subprocess.call(command)
        files_in_archive = None
        observed = None
        archive_path = os.path.join(self.archive_dir, self.zip_filename)
        try:
            print(archive_path)
            zf = zipfile.ZipFile(archive_path, "r")
            files_in_archive = zf.namelist()
            zf.close()
            observed = set([os.path.basename(f) for f in files_in_archive])
        except IOError as ioe:
            print(ioe)
        expected = set(self.file_names)
        self.assertEqual(observed, expected)
        
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        shutil.rmtree(self.archive_dir, ignore_errors=True)
        if os.path.exists(self.zip_filename):
            os.remove(self.zip_filename)
        else:
            print("Zip file must not have been created.")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
