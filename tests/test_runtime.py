import sys
import unittest


class TestRuntime(unittest.TestCase):
    # Assertion should fails if the runtime is less than that version and passes if greater than or equal to
    def test_python_version_311_or_higher(self):
        """
        Test that Python version is 3.11 or higher
        """
        version_info = sys.version_info
        self.assertGreaterEqual(
            version_info.major, 3, "Python major version should be 3 or higher"
        )
        if version_info.major == 3:
            self.assertGreaterEqual(
                version_info.minor,
                11,
                "Python minor version should be 11 or higher for Python 3.x",
            )


if __name__ == "__main__":
    unittest.main()
