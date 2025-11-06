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