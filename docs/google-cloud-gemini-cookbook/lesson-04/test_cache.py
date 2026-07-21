import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
from datetime import datetime, timedelta

# Mocking google.genai before it's imported in cache.py
mock_genai = MagicMock()
sys.modules["google"] = MagicMock()
sys.modules["google.genai"] = mock_genai
sys.modules["google.genai.types"] = MagicMock()

# Add the directory to sys.path to allow relative imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from cache import CacheManager
import config

class TestCacheManager(unittest.TestCase):
    def setUp(self):
        self.cm = CacheManager()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_cache_flag_file_data_file_not_found(self, mock_file):
        cache_name, creation_time, is_valid = self.cm.get_cache_flag_file_data()
        self.assertIsNone(cache_name)
        self.assertIsNone(creation_time)
        self.assertFalse(is_valid)

    @patch("builtins.open", new_callable=mock_open, read_data="Timestamp: 2023-01-01T00:00:00\nCache Name: my-cache\n")
    @patch("cache.datetime")
    def test_get_cache_flag_file_data_valid(self, mock_datetime, mock_file):
        # Mocking datetime.fromisoformat and datetime.now
        mock_datetime.fromisoformat.return_value = datetime(2023, 1, 1, 0, 0, 0)
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 10, 0)

        cache_name, creation_time, is_valid = self.cm.get_cache_flag_file_data()
        self.assertEqual(cache_name, "my-cache")
        self.assertEqual(creation_time, datetime(2023, 1, 1, 0, 0, 0))
        self.assertTrue(is_valid)

    @patch("builtins.open", new_callable=mock_open, read_data="Timestamp: 2023-01-01T00:00:00\nCache Name: my-cache\n")
    @patch("cache.datetime")
    def test_get_cache_flag_file_data_expired(self, mock_datetime, mock_file):
        # Mocking datetime.fromisoformat and datetime.now
        mock_datetime.fromisoformat.return_value = datetime(2023, 1, 1, 0, 0, 0)
        # config.CACHE_TTL_SECONDS is 1800 (30 minutes)
        # So we set now to be 31 minutes after creation
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 31, 0)

        cache_name, creation_time, is_valid = self.cm.get_cache_flag_file_data()
        self.assertEqual(cache_name, "my-cache")
        self.assertEqual(creation_time, datetime(2023, 1, 1, 0, 0, 0))
        self.assertFalse(is_valid)

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_get_cache_flag_file_data_empty_file(self, mock_file):
        cache_name, creation_time, is_valid = self.cm.get_cache_flag_file_data()
        self.assertIsNone(cache_name)
        self.assertIsNone(creation_time)
        self.assertFalse(is_valid)

    @patch("builtins.open", new_callable=mock_open, read_data="Invalid Content\n")
    def test_get_cache_flag_file_data_corrupted_file(self, mock_file):
        cache_name, creation_time, is_valid = self.cm.get_cache_flag_file_data()
        self.assertIsNone(cache_name)
        self.assertIsNone(creation_time)
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
