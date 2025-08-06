import unittest
import tempfile
import os

# from unittest.mock import patch, MagicMock
from lib.verse import common


class TestCommon(unittest.TestCase):
    def test_load_data_csv(self):
        """
        Test loading CSV data
        """
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            f.write("col1,col2\n1,2\n3,4\n")
            temp_path = f.name

        try:
            df = common.load_data(temp_path)
            self.assertEqual(len(df), 2)
            self.assertEqual(list(df.columns), ["col1", "col2"])
        finally:
            os.unlink(temp_path)

    def test_get_memory_usage(self):
        """
        Test memory usage function returns positive float
        """
        memory = common.get_memory_usage()
        self.assertIsInstance(memory, (int, float))
        self.assertGreater(memory, 0)

    def test_elapsed_time_decorator(self):
        """
        Test elapsed time decorator
        """

        @common.elapsed_time
        def dummy_function():
            return "test"

        result = dummy_function()
        self.assertEqual(result, "test")

    def test_profile_memory_decorator(self):
        """
        Test memory profiling decorator
        """

        @common.profile_memory
        def dummy_function():
            return "test"

        result = dummy_function()
        self.assertEqual(result, "test")


if __name__ == "__main__":
    unittest.main()
