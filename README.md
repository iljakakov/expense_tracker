# Išlaidų Sekimo Programos Ataskaita

## 1. Įvadas

### Kas yra mano aplikacija?

Ši aplikacija yra paprasta išlaidų sekimo programa, parašyta Python kalba. Ji leidžia vartotojui įvesti vienkartines ir pasikartojančias išlaidas, peržiūrėti įrašus, ištrinti pasirinktą įrašą ir apskaičiuoti bendrą išleistą sumą.

### Kaip paleisti programą?

Programą galima paleisti terminale su komanda:

```bash
python expense_tracker.py
```

Testus galima paleisti su komanda:

```bash
python -m unittest test_expense_tracker.py
```

### Kaip naudotis programa?

Paleidus programą ekrane rodomas meniu. Vartotojas gali:

1. pridėti vienkartinę išlaidą;
2. pridėti pasikartojančią išlaidą;
3. peržiūrėti visas išlaidas;
4. ištrinti išlaidą pagal ID;
5. pamatyti bendrą sumą;
6. išeiti iš programos.

Duomenys išsaugomi `expenses.csv` faile, todėl uždarius programą jie nedingsta.

## 2. Analizė

### Funkciniai reikalavimai

Programa atitinka pagrindinius funkcinius reikalavimus:

- leidžia pridėti išlaidų įrašus;
- leidžia saugoti ir nuskaityti duomenis iš CSV failo;
- leidžia peržiūrėti įrašus;
- leidžia ištrinti įrašus;
- apskaičiuoja bendrą išleistą sumą.

### 4 OOP principai

#### Abstrakcija

Abstrakcija realizuota naudojant abstrakčią klasę `FinancialRecord`.

```python
class FinancialRecord(ABC):
    @abstractmethod
    def record_type(self) -> str:
        ...
```

Ši klasė apibrėžia bendrą struktūrą visiems finansiniams įrašams, tačiau pati nėra naudojama tiesiogiai. Ji pateikia bendrus laukus ir bendrą sąsają kitoms klasėms.

#### Paveldėjimas

Paveldėjimas panaudotas klasėse `Expense` ir `RecurringExpense`.

```python
class Expense(FinancialRecord):
    ...

class RecurringExpense(Expense):
    ...
```

`Expense` paveldi bendrą logiką iš `FinancialRecord`, o `RecurringExpense` papildomai išplečia `Expense` klasę su `billing_cycle` lauku.

#### Inkapsuliacija

Inkapsuliacija realizuota naudojant privačius laukus ir `property` metodus.

```python
@property
def amount(self) -> float:
    return self._amount

@amount.setter
def amount(self, value: float) -> None:
    if value <= 0:
        raise ValueError("Amount must be greater than 0.")
    self._amount = round(value, 2)
```

Tokiu būdu duomenys yra tikrinami prieš priskyrimą. Tai apsaugo programą nuo neteisingų reikšmių.

#### Polimorfizmas

Polimorfizmas panaudotas dirbant su skirtingais įrašų tipais per tą pačią sąsają.

```python
for record in records:
    print(record.display_text())
```

Nors `records` sąraše gali būti tiek `Expense`, tiek `RecurringExpense` objektai, programa juos apdoroja vienodai. Kiekviena klasė pati nusprendžia, kaip turi atrodyti jos tipas ir atvaizdavimas.

### Projektavimo šablonas

Programoje panaudotas `Factory Method` šablonas.

```python
class RecordFactory:
    @staticmethod
    def create_record(...):
        if normalized_type == "expense":
            return Expense(...)
        if normalized_type == "recurring":
            return RecurringExpense(...)
```

Šis šablonas pasirinktas todėl, kad programoje reikia kurti skirtingų tipų objektus. Vietoje to, kad objektų kūrimo logika būtų išmėtyta skirtingose vietose, ji yra centralizuota vienoje klasėje. Tai daro kodą aiškesnį ir lengviau plečiamą.

`Factory Method` šiuo atveju yra tinkamesnis už, pavyzdžiui, `Singleton`, nes pagrindinis tikslas yra ne vieno objekto egzistavimo užtikrinimas, o skirtingų objektų kūrimas pagal pasirinktą tipą.

### Kompozicija ir agregacija

Kompozicija programoje naudojama taip:

- `ExpenseTrackerApp` sudaryta iš `ExpenseTracker` ir `ConsolePrinter`;
- `ExpenseTracker` naudoja `CSVStorage` duomenims saugoti.

Agregacija programoje matoma per `ExpenseTracker` klasę, kuri saugo finansinių įrašų sąrašą:

```python
self._records = storage.load_records()
```

Šis sąrašas gali turėti kelis skirtingus objektus, kurie egzistuoja kaip atskiri vienetai.

### Skaitymas iš failo ir rašymas į failą

Programa naudoja CSV failą `expenses.csv`.

Skaitymas:

```python
def load_records(self) -> list[FinancialRecord]:
```

Rašymas:

```python
def save_records(self, records: list[FinancialRecord]) -> None:
```

CSV formatas pasirinktas todėl, kad jis yra paprastas, aiškus ir lengvai atidaromas su kitomis programomis, pvz., Excel.

### Testavimas

Pagrindinis funkcionalumas padengtas `unittest` testais faile `test_expense_tracker.py`.

Patikrinti šie atvejai:

- ar `RecordFactory` sukuria teisingą objektą;
- ar teisingai pridedamos išlaidos;
- ar teisingai apskaičiuojama bendra suma;
- ar įrašai ištrinami teisingai;
- ar duomenys sėkmingai išsaugomi ir vėl nuskaityti.

## 3. Rezultatai ir išvados

- Sukurta veikianti išlaidų sekimo programa, kuri leidžia pridėti, saugoti, peržiūrėti ir trinti išlaidų įrašus.
- Programoje sėkmingai įgyvendinti visi keturi objektinio programavimo principai.
- Pasirinktas `Factory Method` šablonas padėjo aiškiai atskirti objektų kūrimo logiką nuo kitos programos logikos.
- Kompozicijos ir agregacijos principai padarė programos struktūrą aiškesnę ir lengviau prižiūrimą.
- Projektą būtų galima plėsti pridedant kategorijų filtravimą, mėnesines ataskaitas, grafinę sąsają arba duomenų bazę vietoje CSV failo.

## 4. Šaltiniai

- Python dokumentacija: [https://docs.python.org/3/](https://docs.python.org/3/)
- PEP 8 stiliaus gairės: [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
