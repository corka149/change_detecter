import unittest
import change_detector
import os
from unittest import TestCase


class TestCore(TestCase):

    def test_change_interval(self):
        fo = change_detector.core.FileObserver(".")
        fo.change_interval(20)
        self.assertEqual(fo.__interval_in_secs__, 20, "Interval was not changed")

    def test_change_runtime(self):
        fo = change_detector.core.FileObserver(".")
        fo.change_runtime(60 * 60)
        self.assertEqual(fo.__runtime__, 3600, "Runtime was not changed")

    def test_read_dir(self):
        fo = change_detector.core.FileObserver(".")
        changed_files = fo.__read_dir__()
        current_dir = os.listdir(".")
        self.assertEqual(len(current_dir), len(changed_files), "FileObserver did not correct changed files")


if __name__ == '__main__':
    unittest.main()
