import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_alussa_oikea_summa(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_lataaminen_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(100)

        self.assertEqual(self.maksukortti.saldo_euroina(), 11)

    def test_rahan_ottaminen_kun_rahaa_tarpeeksi(self):
        self.maksukortti.ota_rahaa(500)

        self.assertEqual(self.maksukortti.saldo_euroina(), 5)
        self.assertEqual(self.maksukortti.ota_rahaa(500), True)

    def test_otetaan_liikaa_rahaa(self):
        self.maksukortti.ota_rahaa(1100)

        self.assertEqual(self.maksukortti.saldo_euroina(), 10)
        self.assertEqual(self.maksukortti.ota_rahaa(1100), False)

    def test_maksukortti_palautus_string(self):

        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

