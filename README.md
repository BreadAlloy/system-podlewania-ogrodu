# system-podlewania-ogrodu

## przydatne komendy

### uruchamianie (bedac w folderze system-podlewania-ogrodu)

```bash
docker compose up --build
```
webapp powinien byc dostepny w `http://localhost:8000` jezeli ktos uzyje WSL to trzeba wstawic ip wsl zamiast localhost

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
