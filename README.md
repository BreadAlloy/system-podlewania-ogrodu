# system-podlewania-ogrodu

## przydatne komendy

### migracje / tworzenie danych

```bash
./database_init.sh
```

### uruchamianie (bez raspberrypi)

```bash
RPI=false docker compose up --build
```
webapp powinien byc dostepny w `http://localhost:8000`

### uruchamianie (na raspberrypi)

```bash
docker compose up --build
```

### usuwanie volumes
```bash
docker compose down -v
```

### testowanie gpio-worker (miejsce skryptu bedzie jeszcze zmienione z `apps/company/management/commands/gpio-worker.py` gdy utworzymy juz oficjalnie aplikacje)
```bash
./manage.sh gpio-worker
```

### tworzenie nowej "aplikacji" ktos to musi zrobic nie mialem dobrego pomyslu na nazwe
```bash
./manage.sh startapp {nazwa_aplikacji} apps/{nazwa_aplikacji}
```
w `settings.py` `INSTALLED_APPS` dodac nowy element `'apps.nazwa_aplikacji'`

### migracje bazy danych (po zmianach)
```bash
./manage.sh makemigrations
./manage.sh migrate
```

## Kontrola sekcji za pomocą gpio gotowa
Jest plik snippetowy testy.py by zobaczyć jak sobie wyobrażam, że sie tego używa. 
jest też konfiguracja.py gdzie możecie włączyć debug_poza_raspberry.
Nie testowałem w innym miejscu niż raspberry więc jeśli nie działa to moja wina
Oczywiście nie pip installujcie requirements_testy.txt na czymś innym niż raspberry.
Też pewnie z requirements_gpio.txt musicie te biblioteki usunąć jeśli inny sprzęt.
Może czegoś brakować w requirements_gpio.txt ale gpiozero jest tak zrobione że mówi czego brakuje.

## Kontrola sekcji przez stronę web prawie gotowa
Ładnie można przełączać na stronie i gpio-worker to odczytuje. Ale pip install dockerowy nie potrafi zainstalować 2 bibliotek koniecznych do kontroli gpio. Sekcje mają nazwy teraz i należało by je dodać do modelu zaworu.

