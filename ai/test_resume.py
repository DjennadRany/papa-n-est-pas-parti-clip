"""Regression tests for unique footage and storyboard ordering."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import produce


def fake_mp4(payload):
    return bytes([0, 0, 0, 24]) + b"ftypisom" + payload * 1024


class ResumeTests(unittest.TestCase):
    def test_distinct_clips_advance_in_storyboard_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(produce, "VIDEO", Path(tmp)):
                (Path(tmp) / "01.mp4").write_bytes(fake_mp4(b"a"))
                (Path(tmp) / "25.mp4").write_bytes(fake_mp4(b"b"))
                self.assertEqual(produce.missing()[0]["id"], 2)

    def test_duplicate_bytes_are_not_counted_twice(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(produce, "VIDEO", Path(tmp)):
                data = fake_mp4(b"a")
                (Path(tmp) / "01.mp4").write_bytes(data)
                (Path(tmp) / "25.mp4").write_bytes(data)
                self.assertEqual(produce.missing()[0]["id"], 25)
                self.assertEqual(len(produce.verified()), 1)

    def test_invalid_mp4_is_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(produce, "VIDEO", Path(tmp)):
                (Path(tmp) / "01.mp4").write_bytes(b"not an mp4" * 2000)
                self.assertEqual(produce.missing()[0]["id"], 1)


if __name__ == "__main__":
    unittest.main()
