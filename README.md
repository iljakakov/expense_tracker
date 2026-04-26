# Expense tracker    

## 1. Įvadas

### 1.1 Programos tikslas

Šios programos tikslas yra padėti vartotojui registruoti ir valdyti savo finansinius įrašus. Programa leidžia pridėti naujus įrašus, peržiūrėti jau išsaugotus duomenis, ištrinti pasirinktą įrašą bei apskaičiuoti bendrą finansinį rezultatą. Programa palaiko ne tik išlaidas, bet ir pajamas, todėl galima matyti tikslesnį bendrą balansą.

### 1.2 Ka daro ši programa?

Tai yra konsolinė programa, parašyta Python kalba. Ji skirta paprastam asmeninių finansų sekimui. Programa veikia terminale, todėl jai nereikia grafinės vartotojo sąsajos ar išorinių bibliotekų. Visi duomenys saugomi CSV faile, todėl informacija išlieka ir uždarius programą.

### 1.3 Kaip paleisti programą?

Norint paleisti programą, reikia:

1. Turėti įdiegtą Python interpretatorių.
2. Išsaugoti kodą faile `expense_tracker.py`.
3. Terminale paleisti komandą:

```bash
python expense_tracker.py
```

### 1.4 Kaip naudotis programa?

Paleidus programą vartotojui pateikiamas meniu su šiais pasirinkimais:

1. `Pridėti įrašą` – leidžia įvesti naują finansinį įrašą.
2. `Rodyti įrašus` – parodo visus išsaugotus įrašus.
3. `Ištrinti įrašą` – pašalina pasirinktą įrašą pagal jo ID.
4. `Rodyti bendrą sumą` – apskaičiuoja bendrą rezultatą, įtraukiant išlaidas ir pajamas.
5. `Išeiti` – užbaigia programos darbą.

Norint įvesti pajamas, vartotojas gali pasirinkti kategoriją `Pajamos`. Tokiu atveju įrašas bus apdorojamas kitaip nei įprasta išlaida.

## 2. Programos analizė

### 2.1 Programos veikimo principas

Programa paremta klase `IslaiduSekiklis`, kuri valdo pagrindinę logiką:

- nuskaito duomenis iš CSV failo;
- išsaugo duomenis į CSV failą;
- prideda naujus įrašus;
- rodo visų įrašų sąrašą;
- ištrina pasirinktą įrašą;
- apskaičiuoja bendrą finansinį rezultatą.

Programoje duomenys saugomi faile `islaidos.csv`, todėl informacija išlieka net ir uždarius programą.

### 2.2 Duomenų skaitymas iš failo ir rašymas į failą

Duomenų failas apibrėžiamas taip:

```python
DUOMENU_FAILAS = Path("islaidos.csv")
```

Duomenų nuskaitymas vyksta metode `ikrauti_islaidas()`:

```python
with self.failo_vardas.open("r", encoding="utf-8", newline="") as failas:
    skaitytuvas = csv.DictReader(failas)
```

Duomenų išsaugojimas vyksta metode `issaugoti_islaidas()`:

```python
with self.failo_vardas.open("w", encoding="utf-8", newline="") as failas:
    rasytuvas = csv.DictWriter(failas, fieldnames=laukai)
```

CSV formatas pasirinktas todėl, kad jis yra paprastas, aiškus ir tinkamas mažos apimties projektui.

### 2.3 Objektinio programavimo principai

#### Abstrakcija

Šioje programoje abstrakcija atsiskleidžia per klases `Islaida` ir `Pajamos`, kurios aprašo bendrą finansinio įrašo idėją. Abi klasės saugo informaciją apie sumą, kategoriją ir datą bei turi metodą `gauti_suma()`, kuris naudojamas bendram rezultatui apskaičiuoti.

```python
class Islaida:
    def __init__(self, suma, kategorija, data):
        self.suma = float(suma)
        self.kategorija = kategorija
        self.data = data
```

#### Paveldėjimas

Paveldėjimas programoje realizuotas taip, kad klasė `Pajamos` paveldi klasę `Islaida`.

```python
class Pajamos(Islaida):
    def gauti_suma(self):
        return -self.suma
```

Tai leidžia pakartotinai naudoti pagrindinius laukus ir logiką, tačiau prireikus pakeisti elgseną.

#### Inkapsuliacija

Inkapsuliacija programoje įgyvendinama per klasių metodus, kurie tvarko duomenų įkėlimą, išsaugojimą, ištrynimą ir bendros sumos skaičiavimą. Vartotojas neturi tiesiogiai dirbti su failu ar vidiniu sąrašu – viskas atliekama per klasės metodus:

- `ikrauti_islaidas()`
- `issaugoti_islaidas()`
- `prideti_islaida()`
- `istrinti_islaida()`
- `rodyti_bendra_suma()`

Tokiu būdu programos vidinė logika yra paslėpta, o valdymas vyksta per aiškiai apibrėžtas funkcijas.

#### Polimorfizmas

Polimorfizmas realizuotas metode `rodyti_bendra_suma()`. Programa sukuria objektą pagal įrašo kategoriją ir tada kviečia tą patį metodą `gauti_suma()`.

```python
for islaida in self.islaidos:
    obj = self.sukurti_objekta(islaida)
    bendra_suma += obj.gauti_suma()
```

Jeigu objektas yra `Islaida`, grąžinama teigiama suma. Jeigu objektas yra `Pajamos`, grąžinama neigiama suma. Taigi tas pats metodas veikia skirtingai priklausomai nuo objekto tipo.

### 2.4 Naudotas projektavimo šablonas

Programoje panaudotas `Singleton` projektavimo šablonas.

```python
class IslaiduSekiklis:
    _instance = None

    def __new__(cls, failo_vardas):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

Šis šablonas užtikrina, kad programoje egzistuotų tik vienas `IslaiduSekiklis` objektas. Toks sprendimas tinkamas todėl, kad visa programa remiasi vienu centriniu sekikliu, kuris valdo tą patį duomenų failą ir vieną įrašų sąrašą.

`Singleton` šablonas šiuo atveju tinka labiau nei, pavyzdžiui, `Factory Method`, nes svarbiausias tikslas yra turėti vieną bendrą sistemos valdymo tašką, o ne kurti daug skirtingų valdančių objektų.

### 2.5 Kompozicija ir agregacija

Kompozicija programoje matoma tuo, kad `IslaiduSekiklis` klasė dirba su savo vidiniu įrašų sąrašu `self.islaidos` ir yra atsakinga už jo valdymą.

Agregacija matoma per metodą `sukurti_objekta()`, kuris pagal duomenis sukuria `Islaida` arba `Pajamos` objektą:

```python
def sukurti_objekta(self, islaida):
    if islaida["kategorija"].lower() == "pajamos":
        return Pajamos(islaida["suma"], islaida["kategorija"], islaida["data"])
    return Islaida(islaida["suma"], islaida["kategorija"], islaida["data"])
```

Tai reiškia, kad sekiklis dirba su kitais objektais ir panaudoja juos bendram tikslui pasiekti.

### 2.6 Pagrindiniai metodai

#### `ikrauti_islaidas()`

Nuskaito informaciją iš CSV failo ir įkelia ją į vidinį sąrašą.

#### `issaugoti_islaidas()`

Išsaugo visus esamus įrašus į CSV failą.

#### `sukurti_objekta()`

Pagal kategoriją nusprendžia, ar turi būti sukurtas `Islaida`, ar `Pajamos` objektas.

#### `prideti_islaida()`

Leidžia vartotojui įvesti naują įrašą ir išsaugo jį faile.

#### `rodyti_islaidas()`

Parodo visus įrašus terminale.

#### `istrinti_islaida()`

Leidžia pašalinti pasirinktą įrašą pagal jo ID.

#### `rodyti_bendra_suma()`

Apskaičiuoja bendrą rezultatą naudojant polimorfizmą.

#### `sutvarkyti_id()`

Po įrašo ištrynimo atnaujina visus ID, kad jie išliktų nuoseklūs.

## 3. Funkciniai reikalavimai

Programa įgyvendina šias funkcijas:

- naujų įrašų pridėjimą;
- įrašų peržiūrą;
- įrašų trynimą;
- bendros sumos apskaičiavimą;
- duomenų saugojimą faile;
- duomenų nuskaitymą iš failo.

Be to, programa išskiria pajamas ir išlaidas, todėl gali tiksliau apskaičiuoti galutinį finansinį rezultatą.

## 4. Testavimas

Programos pagrindinis funkcionalumas turėtų būti testuojamas naudojant `unittest` karkasą. Galima tikrinti:

- ar įrašas sėkmingai pridedamas;
- ar įrašas teisingai ištrinamas;
- ar bendros sumos skaičiavimas veikia teisingai;
- ar duomenys sėkmingai įrašomi į failą ir nuskaitomi iš jo.

Testavimas svarbus todėl, kad leidžia greičiau aptikti logikos klaidas ir užtikrina programos stabilumą.

## 5. Kodo stilius

Programa parašyta Python kalba ir remiasi standartinėmis bibliotekomis:

- `csv` – darbui su CSV failais;
- `pathlib.Path` – failo keliui aprašyti;
- `datetime` – dabartinei datai gauti.

Kodas suskirstytas į klases ir metodus, todėl jį lengviau suprasti, prižiūrėti ir plėsti. Pavadinimai parinkti prasmingi ir atitinka jų paskirtį.

## 6. Rezultatai

- Sukurta veikianti konsolinė finansinių įrašų sekimo programa.
- Programa leidžia registruoti tiek išlaidas, tiek pajamas.
- Sėkmingai įgyvendinti visi keturi objektinio programavimo principai.
- Programoje panaudotas `Singleton` projektavimo šablonas.
- Duomenys saugomi CSV faile, todėl informacija neprarandama uždarius programą.

## 7. Išvados

Šiame darbe sukurta Python programa leidžia patogiai sekti asmeninius finansinius įrašus. Programa atitinka pagrindinius funkcinius reikalavimus: leidžia pridėti, rodyti, trinti įrašus bei apskaičiuoti bendrą sumą. Papildomai ji išskiria pajamas ir išlaidas, todėl bendras rezultatas apskaičiuojamas tiksliau.

Programoje įgyvendinti objektinio programavimo principai, panaudotas `Singleton` projektavimo šablonas, o duomenų saugojimui pasirinktas CSV failas. Ateityje programą būtų galima plėsti pridedant filtravimą pagal datą, kategorijų statistiką, ataskaitų generavimą arba grafinę vartotojo sąsają.

## 8. Naudoti šaltiniai

- Python oficiali dokumentacija: [https://docs.python.org/3/](https://docs.python.org/3/)
- CSV modulio dokumentacija: [https://docs.python.org/3/library/csv.html](https://docs.python.org/3/library/csv.html)
- Pathlib dokumentacija: [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)
- Datetime dokumentacija: [https://docs.python.org/3/library/datetime.html](https://docs.python.org/3/library/datetime.html)
