import csv
from pathlib import Path
from datetime import datetime


DUOMENU_FAILAS = Path("islaidos.csv")


class Islaida:
    def __init__(self, suma, kategorija, data):
        self.suma = float(suma)
        self.kategorija = kategorija
        self.data = data

    def gauti_suma(self):
        return self.suma


class Pajamos(Islaida):
    def gauti_suma(self):
        return -self.suma


class IslaiduSekiklis:
    _instance = None

    def __new__(cls, failo_vardas):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, failo_vardas):
        if hasattr(self, "_initialized"):
            return

        self.failo_vardas = failo_vardas
        self.islaidos = []
        self.ikrauti_islaidas()
        self._initialized = True

    def ikrauti_islaidas(self):
        if not self.failo_vardas.exists():
            return

        with self.failo_vardas.open("r", encoding="utf-8", newline="") as failas:
            skaitytuvas = csv.DictReader(failas)
            self.islaidos = []

            for eilute in skaitytuvas:
                nauja_eilute = {
                    "id": eilute.get("id", ""),
                    "suma": eilute.get("suma", ""),
                    "kategorija": eilute.get("kategorija", "Bendra"),
                    "data": eilute.get("data", datetime.now().strftime("%Y-%m-%d")),
                }
                self.islaidos.append(nauja_eilute)

    def issaugoti_islaidas(self):
        with self.failo_vardas.open("w", encoding="utf-8", newline="") as failas:
            laukai = ["id", "suma", "kategorija", "data"]
            rasytuvas = csv.DictWriter(failas, fieldnames=laukai)
            rasytuvas.writeheader()
            rasytuvas.writerows(self.islaidos)

    def sukurti_objekta(self, islaida):
        if islaida["kategorija"].lower() == "pajamos":
            return Pajamos(islaida["suma"], islaida["kategorija"], islaida["data"])
        return Islaida(islaida["suma"], islaida["kategorija"], islaida["data"])

    def prideti_islaida(self):
        suma = input("Įveskite sumą: ").strip()
        kategorija = input("Įveskite kategoriją: ").strip()

        try:
            suma = float(suma)
            if suma <= 0:
                print("Suma turi būti didesnė už 0.")
                return
        except ValueError:
            print("Neteisinga suma.")
            return

        data = datetime.now().strftime("%Y-%m-%d")

        islaida = {
            "id": str(len(self.islaidos) + 1),
            "suma": f"{suma:.2f}",
            "kategorija": kategorija if kategorija else "Bendra",
            "data": data,
        }

        self.islaidos.append(islaida)
        self.issaugoti_islaidas()
        print("Įrašas sėkmingai pridėtas.")

    def rodyti_islaidas(self):
        if not self.islaidos:
            print("Įrašų nerasta.")
            return

        print("\nĮrašai:")
        for islaida in self.islaidos:
            print(
                f"ID: {islaida['id']} | "
                f"Suma: EUR {islaida['suma']} | "
                f"Kategorija: {islaida['kategorija']} | "
                f"Data: {islaida['data']}"
            )

    def istrinti_islaida(self):
        islaidos_id = input("Įveskite įrašo ID, kurį norite ištrinti: ").strip()

        for islaida in self.islaidos:
            if islaida["id"] == islaidos_id:
                self.islaidos.remove(islaida)
                self.sutvarkyti_id()
                self.issaugoti_islaidas()
                print("Įrašas ištrintas.")
                return

        print("Įrašas nerastas.")

    def rodyti_bendra_suma(self):
        bendra_suma = 0

        for islaida in self.islaidos:
            obj = self.sukurti_objekta(islaida)
            bendra_suma += obj.gauti_suma()

        print(f"Bendra išlaidų suma: EUR {bendra_suma:.2f}")

    def sutvarkyti_id(self):
        for indeksas, islaida in enumerate(self.islaidos, start=1):
            islaida["id"] = str(indeksas)


def pagrindine_programa():
    sekiklis = IslaiduSekiklis(DUOMENU_FAILAS)

    while True:
        print(
            "\nIšlaidų sekiklis\n"
            "1. Pridėti įrašą\n"
            "2. Rodyti įrašus\n"
            "3. Ištrinti įrašą\n"
            "4. Rodyti bendrą sumą\n"
            "5. Išeiti"
        )

        pasirinkimas = input("Pasirinkite veiksmą: ").strip()

        if pasirinkimas == "1":
            sekiklis.prideti_islaida()
        elif pasirinkimas == "2":
            sekiklis.rodyti_islaidas()
        elif pasirinkimas == "3":
            sekiklis.istrinti_islaida()
        elif pasirinkimas == "4":
            sekiklis.rodyti_bendra_suma()
        elif pasirinkimas == "5":
            print("Viso gero!")
            break
        else:
            print("Neteisingas pasirinkimas.")


if __name__ == "__main__":
    pagrindine_programa()
