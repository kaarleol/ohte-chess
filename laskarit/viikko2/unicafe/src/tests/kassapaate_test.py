import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):   
        self.kassapaate = Kassapaate()
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kassapaate_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_kassapaate_luotu_oikein(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_syo_edullisesti_kateisella_toimii_kun_rahaa_tarpeeksi(self):
        self.kassapaate.syo_edullisesti_kateisella(250)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(250), 10)

    def test_syo_edullisesti_kateisella_toimii_kun_rahaa_liian_vahan(self):
        self.kassapaate.syo_edullisesti_kateisella(230)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(230), 230)

    def test_syo_maukkaasti_kateisella_toimii_kun_rahaa_tarpeeksi(self):
        self.kassapaate.syo_maukkaasti_kateisella(410)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(410), 10)

    def test_syo_maukkaasti_kateisella_toimii_kun_rahaa_liian_vahan(self):
        self.kassapaate.syo_maukkaasti_kateisella(390)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(390), 390)

    def test_syo_edullisesti_kortilla_toimii_kun_rahaa_tarpeeksi(self):
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.maksukortti.saldo_euroina(), 7.6)

    def test_syo_edullisesti_kortilla_toimii_kun_rahaa_liian_vahan(self):
        self.maksukortti=Maksukortti(230)
        self.kassapaate.syo_edullisesti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.maksukortti.saldo_euroina(), 2.3)

    def test_syo_maukkaasti_kortilla_toimii_kun_rahaa_tarpeeksi(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.maksukortti.saldo_euroina(), 6)

    def test_syo_maukkaasti_kortilla_toimii_kun_rahaa_liian_vahan(self):
        self.maksukortti=Maksukortti(390)
        self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.maksukortti.saldo_euroina(), 3.9)

    def test_rahan_lataaminen_kortille_toimii_oikein(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 500)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1005)
        self.assertEqual(self.maksukortti.saldo_euroina(), 15)

    def test_rahan_lataaminen_kortille_negatiivinen(self):
        self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -500)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)



