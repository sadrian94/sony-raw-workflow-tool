import unittest
from unittest.mock import patch
from copy_arw import find_matching_arw, validate_dirs

class TestCopyArw(unittest.TestCase):
    def test_find_matching_arw_exact(self):
        backup_files = ["DSC00571.ARW", "DSC00572.ARW"]
        self.assertEqual(find_matching_arw("DSC00571.JPG", backup_files), "DSC00571.ARW")

    def test_find_matching_arw_case_insensitive(self):
        backup_files = ["dsc00571.arw", "DSC00572.ARW"]
        self.assertEqual(find_matching_arw("DSC00571.jpg", backup_files), "dsc00571.arw")

    def test_find_matching_arw_not_found(self):
        backup_files = ["DSC00572.ARW"]
        self.assertIsNone(find_matching_arw("DSC00571.JPG", backup_files))

    @patch('os.path.isdir')
    def test_validate_dirs_all_exist(self, mock_isdir):
        mock_isdir.return_value = True
        self.assertEqual(validate_dirs("dummy_path"), [])

    @patch('os.path.isdir')
    def test_validate_dirs_some_missing(self, mock_isdir):
        # Let's say JPG and ARW exist, but backup is missing
        # validate_dirs checks 'JPG', 'backup', 'ARW'
        mock_isdir.side_effect = lambda path: not path.endswith('backup')
        self.assertEqual(validate_dirs("dummy_path"), ["backup"])


if __name__ == "__main__":
    unittest.main()
