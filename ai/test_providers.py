import unittest
from providers import available_providers, ShotRequest
class TestProviderRegistry(unittest.TestCase):
    def test_only_existing_provider_is_active(self):
        p=available_providers()
        self.assertTrue(p["wan_hf"]["implemented"])
        self.assertFalse(p["minimax_h3"]["implemented"])
    def test_request_contract(self):
        from pathlib import Path
        r=ShotRequest(1,Path("01.jpg"),"walk",4.0,42)
        self.assertEqual(r.scene_id,1)
if __name__=="__main__":unittest.main()
