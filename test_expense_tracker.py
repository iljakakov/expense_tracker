import unittest
import tempfile
from pathlib import Path

from expense_tracker import IslaiduSekiklis, Islaida, Pajamos


class TestExpenseTracker(unittest.TestCase):
    def setUp(self):
        IslaiduSekiklis._instance = None
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        self.file_path = Path(self.temp_file.name)
        self.temp_file.close()
        self.tracker = IslaiduSekiklis(self.file_path)

    def tearDown(self):
        if self.file_path.exists():
            self.file_path.unlink()
        IslaiduSekiklis._instance = None

    def test_singleton(self):
        tracker2 = IslaiduSekiklis(self.file_path)
        self.assertIs(self.tracker, tracker2)

    def test_islaida_suma(self):
        islaida = Islaida(100, "maistas", "2026-04-26")
        self.assertEqual(islaida.gauti_suma(), 100)

    def test_pajamos_suma(self):
        pajamos = Pajamos(50, "pajamos", "2026-04-26")
        self.assertEqual(pajamos.gauti_suma(), -50)

    def test_sukurti_objekta_islaida(self):
        duomenys = {
            "id": "1",
            "suma": "20.00",
            "kategorija": "maistas",
            "data": "2026-04-26",
        }
        obj = self.tracker.sukurti_objekta(duomenys)
        self.assertIsInstance(obj, Islaida)
        self.assertEqual(obj.gauti_suma(), 20)

    def test_sukurti_objekta_pajamos(self):
        duomenys = {
            "id": "2",
            "suma": "50.00",
            "kategorija": "pajamos",
            "data": "2026-04-26",
        }
        obj = self.tracker.sukurti_objekta(duomenys)
        self.assertIsInstance(obj, Pajamos)
        self.assertEqual(obj.gauti_suma(), -50)

    def test_save_and_load(self):
        self.tracker.islaidos.append({
            "id": "1",
            "suma": "30.00",
            "kategorija": "transportas",
            "data": "2026-04-26",
        })

        self.tracker.issaugoti_islaidas()

        IslaiduSekiklis._instance = None
        naujas_tracker = IslaiduSekiklis(self.file_path)

        self.assertEqual(len(naujas_tracker.islaidos), 1)
        self.assertEqual(naujas_tracker.islaidos[0]["kategorija"], "transportas")
        self.assertEqual(naujas_tracker.islaidos[0]["suma"], "30.00")


if __name__ == "__main__":
    unittest.main()
