# Expense tracker

## 1. Įvadas

### 1.1 Programos tikslas

Šios programos tikslas yra padėti vartotojui sekti savo kasdienes išlaidas. Programa leidžia pridėti naujas išlaidas, peržiūrėti jau įvestus įrašus, ištrinti pasirinktą įrašą bei apskaičiuoti bendrą visų išlaidų sumą.

### 1.2 Ka daro ši programa?

Tai yra konsolinė Python programa, skirta paprastam išlaidų valdymui. Ji veikia terminale, todėl nereikalauja grafinės sąsajos ar papildomų bibliotekų. Visi duomenys saugomi CSV faile, todėl programa yra lengvai suprantama ir paprasta naudoti.

### 1.3 Kaip paleisti programą?

Norint paleisti programą, reikia:

1. Turėti įdiegtą Python.
2. Išsaugoti programos kodą faile, pavyzdžiui, `expense_tracker.py`.
3. Terminale paleisti komandą:

```bash
python expense_tracker.py
```

### 1.4 Kaip naudotis programa?

Paleidus programą vartotojui parodomas meniu su pasirinkimais:

1. `Pridėti išlaidą` – leidžia įvesti naują išlaidą.
2. `Rodyti išlaidas` – parodo visas išsaugotas išlaidas.
3. `Ištrinti išlaidą` – leidžia pašalinti pasirinktą išlaidą pagal jos ID.
4. `Rodyti bendrą sumą` – apskaičiuoja visų išlaidų sumą.
5. `Išeiti` – uždaro programą.

## 2. Programos analizė

### 2.1 Programos veikimo principas

Programa sukurta naudojant klasę `IslaiduSekiklis`, kuri atsakinga už visą pagrindinę logiką. Ši klasė:

- įkelia duomenis iš CSV failo;
- išsaugo duomenis į CSV failą;
- prideda naujas išlaidas;
- parodo išlaidų sąrašą;
- ištrina pasirinktą išlaidą;
- apskaičiuoja bendrą išlaidų sumą.

Programa saugo duomenis faile `islaidos.csv`, todėl uždarius programą informacija išlieka.

### 2.2 Duomenų skaitymas ir rašymas į failą

Programoje naudojamas CSV failo formatas. Duomenų failas apibrėžtas taip:

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

CSV formatas pasirinktas todėl, kad jis yra paprastas, lengvai suprantamas ir patogus mažos apimties duomenims saugoti.

### 2.3 Klasės panaudojimas

Pagrindinė programos klasė yra:

```python
class IslaiduSekiklis:
```

Šios klasės objektas sukuriamas pagrindinėje funkcijoje:

```python
sekiklis = IslaiduSekiklis(DUOMENU_FAILAS)
```

Tai leidžia tvarkingai atskirti duomenų valdymo logiką nuo vartotojo meniu.

### 2.4 Metodų paaiškinimas

#### `ikrauti_islaidas()`

Šis metodas nuskaito informaciją iš CSV failo ir įkelia ją į sąrašą `self.islaidos`.

#### `issaugoti_islaidas()`

Šis metodas įrašo visas esamas išlaidas į CSV failą.

#### `prideti_islaida()`

Leidžia vartotojui įvesti sumą ir kategoriją. Programa patikrina, ar suma yra teisinga ir didesnė už nulį, tada sukuria naują įrašą.

#### `rodyti_islaidas()`

Parodo visas išlaidas ekrane.

#### `istrinti_islaida()`

Leidžia ištrinti įrašą pagal jo ID.

#### `rodyti_bendra_suma()`

Apskaičiuoja ir parodo bendrą visų išlaidų sumą.

#### `sutvarkyti_id()`

Po ištrynimo atnaujina ID reikšmes, kad jos būtų nuoseklios.

## 3. Funkciniai reikalavimai

Programa įgyvendina šias pagrindines funkcijas:

- naujų išlaidų pridėjimą;
- išlaidų rodymą;
- išlaidų trynimą;
- bendros sumos skaičiavimą;
- duomenų saugojimą faile;
- duomenų nuskaitymą iš failo.

## 4. Kodo kokybė ir stilius

Programa parašyta Python kalba ir naudoja aiškius metodų bei kintamųjų pavadinimus lietuvių kalba. Kode logika suskirstyta į atskirus metodus, todėl programą lengviau skaityti ir prižiūrėti.

Naudotos standartinės Python bibliotekos:

- `csv` – darbui su CSV failais;
- `pathlib.Path` – failo keliui aprašyti;
- `datetime` – datos generavimui.

## 5. Rezultatai

- Sukurta veikianti konsolinė išlaidų sekimo programa.
- Vartotojas gali pridėti, peržiūrėti ir ištrinti išlaidas.
- Programa teisingai apskaičiuoja bendrą išlaidų sumą.
- Duomenys saugomi CSV faile, todėl informacija neprarandama uždarius programą.
- Programa yra paprasta, aiški ir lengvai plečiama ateityje.

## 6. Išvados

Šiame darbe buvo sukurta paprasta išlaidų sekimo programa naudojant Python kalbą. Programa leidžia atlikti pagrindinius finansinių įrašų valdymo veiksmus ir saugo duomenis CSV faile. Toks sprendimas yra patogus mažam projektui, nes nereikalauja sudėtingos duomenų bazės ar papildomų technologijų.

Ateityje programą būtų galima išplėsti pridedant:

- išlaidų filtravimą pagal datą;
- išlaidų skirstymą pagal daugiau kategorijų;
- mėnesines ar savaitines ataskaitas;
- grafinę vartotojo sąsają;
- duomenų bazės panaudojimą vietoje CSV failo.

## 7. Naudoti šaltiniai

- Python oficiali dokumentacija: [https://docs.python.org/3/](https://docs.python.org/3/)
- CSV modulio dokumentacija: [https://docs.python.org/3/library/csv.html](https://docs.python.org/3/library/csv.html)
- Pathlib dokumentacija: [https://docs.python.org/3/library/pathlib.html](https://docs.python.org/3/library/pathlib.html)
