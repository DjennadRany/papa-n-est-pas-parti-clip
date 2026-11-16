"""Fast smoke tests for movie configuration; runs without a GPU."""
import json
import tempfile
import unittest
from pathlib import Path
from PIL import Image
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from prepare_images import clean

ROOT=Path(__file__).resolve().parents[1]
class PipelineTests(unittest.TestCase):
    def test_all_images_and_audio_present(self):
        data=json.loads((ROOT/"scenes.json").read_text(encoding="utf-8"))
        self.assertEqual(len(data["scenes"]),48)
        self.assertEqual(sorted(x["id"] for x in data["scenes"]),list(range(1,49)))
        ordered=sorted(data["scenes"],key=lambda x:x["start"])
        self.assertAlmostEqual(ordered[0]["start"],0,places=4)
        for current,following in zip(ordered,ordered[1:]):
            self.assertAlmostEqual(current["end"],following["start"],places=3)
        self.assertAlmostEqual(ordered[-1]["end"],data["duration_seconds"],places=3)
        for s in ordered:
            self.assertTrue((ROOT/"public"/s["image"]).is_file(),s["image"])
        self.assertTrue((ROOT/"public/assets/audio/Papa n'est pas parti(1).mp3").is_file())
    def test_label_cleaning_does_not_change_original(self):
        import hashlib
        sample=ROOT/"public/assets/images/25.jpg"
        original=hashlib.sha256(sample.read_bytes()).digest()
        with tempfile.TemporaryDirectory() as temp:
            dst=Path(temp)/"25.jpg"
            self.assertGreater(clean(sample,dst),0)
            img=Image.open(dst)
            self.assertGreater(img.width,0)
            self.assertEqual(hashlib.sha256(sample.read_bytes()).digest(),original)
if __name__=="__main__":unittest.main()
