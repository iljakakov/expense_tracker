import csv
from pathlib import Path
from datetime import datetime


DUOMENU_FAILAS = Path("islaidos.csv")


class IslaiduSekiklis:
    def __init__(self, failo_vardas):
        self.failo_vardas = failo_vardas
        self.islaidos = []
        self.ikrauti_islaidas()

    def ikrauti_islaidas(self):
        if not self.failo_vardas.exists():
            return

        with self.failo_vardas.open("r", encoding="utf-8", newline="") as failas:
            skaitytuvas = csv.DictReader(failas)
            self.islaidos = []

            for eilute in skaitytuvas:
                nauja_eilute = {
                    "id": eilute.get("id", ""),
                    "suma": eilute.get("suma", eilute.get("amount", "")),
                    "kategorija": eilute.get("kategorija", eilute.get("category", "Bendra")),
                    "data": eilute.get("data", datetime.now().strftime("%Y-%m-%d")),
                }
                self.islaidos.append(nauja_eilute)

    def issaugoti_islaidas(self):
        with self.failo_vardas.open("w", encoding="utf-8", newline="") as failas:
            laukai = ["id", "suma", "kategorija", "data"]
            rasytuvas = csv.DictWriter(failas, fieldnames=laukai)
            rasytuvas.writeheader()
            rasytuvas.writerows(self.islaidos)

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
        print("Išlaida sėkmingai pridėta.")

    def rodyti_islaidas(self):
        if not self.islaidos:
            print("Išlaidų nerasta.")
            return

        print("\nIšlaidos:")
        for islaida in self.islaidos:
            print(
                f"ID: {islaida['id']} | "
                f"Suma: EUR {islaida['suma']} | "
                f"Kategorija: {islaida['kategorija']} | "
                f"Data: {islaida['data']}"
            )

    def istrinti_islaida(self):
        islaidos_id = input("Įveskite išlaidos ID, kurią norite ištrinti: ").strip()

        for islaida in self.islaidos:
            if islaida["id"] == islaidos_id:
                self.islaidos.remove(islaida)
                self.sutvarkyti_id()
                self.issaugoti_islaidas()
                print("Išlaida ištrinta.")
                return

        print("Išlaida nerasta.")

    def rodyti_bendra_suma(self):
        bendra_suma = sum(float(islaida["suma"]) for islaida in self.islaidos)
        print(f"Bendra išlaidų suma: EUR {bendra_suma:.2f}")

    def sutvarkyti_id(self):
        for indeksas, islaida in enumerate(self.islaidos, start=1):
            islaida["id"] = str(indeksas)


def pagrindine_programa():
    sekiklis = IslaiduSekiklis(DUOMENU_FAILAS)

    while True:
        print(
            "\nIšlaidų sekiklis\n"
            "1. Pridėti išlaidą\n"
            "2. Rodyti išlaidas\n"
            "3. Ištrinti išlaidą\n"
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