import unittest
import os
import shutil
import tempfile
import sys
from photo_tool_core import SonyWorkflowManager

class TestSonyWorkflowManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.test_dir)
        
    def test_initialize_album(self):
        # Create dummy camera files
        open(os.path.join(self.test_dir, "DSC00001.JPG"), "w").close()
        open(os.path.join(self.test_dir, "DSC00001.ARW"), "w").close()
        # Create a script file that should be excluded
        open(os.path.join(self.test_dir, "script.py"), "w").close()
        open(os.path.join(self.test_dir, "readme.md"), "w").close()
        
        manager = SonyWorkflowManager(self.test_dir)
        success, moved, copied = manager.initialize_album()
        
        self.assertTrue(success)
        self.assertEqual(moved, 2)
        self.assertEqual(copied, 1)
        
        # Verify folder architecture
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "backup")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "JPG")))
        self.assertTrue(os.path.isdir(os.path.join(self.test_dir, "ARW")))
        
        # Verify files moved to backup
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "backup", "DSC00001.JPG")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "backup", "DSC00001.ARW")))
        
        # Verify script files left untouched
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "script.py")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "readme.md")))
        
        # Verify JPG copied
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "JPG", "DSC00001.JPG")))

if __name__ == "__main__":
    unittest.main()
