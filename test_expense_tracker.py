import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from expense_tracker import IslaiduSekiklis


class IslaiduSekiklisTestai(unittest.TestCase):
    def setUp(self) -> None:
        self.laikinas_katalogas = tempfile.TemporaryDirectory()
        self.failo_kelias = Path(self.laikinas_katalogas.name) / "test_islaidos.csv"
        self.sekiklis = IslaiduSekiklis(self.failo_kelias)

    def tearDown(self) -> None:
        self.laikinas_katalogas.cleanup()

    def test_prideti_islaida(self) -> None:
        with patch("builtins.input", side_effect=["12.50", "Maistas"]):
            self.sekiklis.prideti_islaida()

        self.assertEqual(len(self.sekiklis.islaidos), 1)
        self.assertEqual(self.sekiklis.islaidos[0]["suma"], "12.50")
        self.assertEqual(self.sekiklis.islaidos[0]["kategorija"], "Maistas")

    def test_bendra_suma(self) -> None:
        self.sekiklis.islaidos = [
            {"id": "1", "suma": "10.00", "kategorija": "Maistas", "data": "2026-04-18"},
            {"id": "2", "suma": "5.50", "kategorija": "Transportas", "data": "2026-04-18"},
        ]

        bendra_suma = sum(float(islaida["suma"]) for islaida in self.sekiklis.islaidos)

        self.assertEqual(bendra_suma, 15.50)

    def test_istrinti_islaida(self) -> None:
        self.sekiklis.islaidos = [
            {"id": "1", "suma": "10.00", "kategorija": "Maistas", "data": "2026-04-18"},
            {"id": "2", "suma": "7.00", "kategorija": "Pramogos", "data": "2026-04-18"},
        ]

        with patch("builtins.input", return_value="1"):
            self.sekiklis.istrinti_islaida()

        self.assertEqual(len(self.sekiklis.islaidos), 1)
        self.assertEqual(self.sekiklis.islaidos[0]["id"], "1")
        self.assertEqual(self.sekiklis.islaidos[0]["kategorija"], "Pramogos")

    def test_issaugoti_ir_ikrauti_islaidas(self) -> None:
        self.sekiklis.islaidos = [
            {"id": "1", "suma": "20.00", "kategorija": "Mokesciai", "data": "2026-04-18"},
        ]
        self.sekiklis.issaugoti_islaidas()

        naujas_sekiklis = IslaiduSekiklis(self.failo_kelias)

        self.assertEqual(len(naujas_sekiklis.islaidos), 1)
        self.assertEqual(naujas_sekiklis.islaidos[0]["suma"], "20.00")
        self.assertEqual(naujas_sekiklis.islaidos[0]["kategorija"], "Mokesciai")

    def test_failas_sukuriamas_su_teisingomis_antrastemis(self) -> None:
        self.sekiklis.islaidos = [
            {"id": "1", "suma": "9.99", "kategorija": "Kita", "data": "2026-04-18"},
        ]
        self.sekiklis.issaugoti_islaidas()

        with self.failo_kelias.open("r", encoding="utf-8", newline="") as failas:
            skaitytuvas = csv.DictReader(failas)
            self.assertEqual(skaitytuvas.fieldnames, ["id", "suma", "kategorija", "data"])


if __name__ == "__main__":
    unittest.main()
