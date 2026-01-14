# Nowa komenda by uruchomić:
```bash

RPI=true AKTYWUJ_KOMUNIKATOR=true docker compose up

```

# STEROWNIK PODLEWANIA OGRODU - USER GUIDE 

Wersja 0.0.0.1.0 
Wydanie 8.01.2026 
Autorzy: Krzysztof Kupczyk, Filip Kojro, Dawid Antkowiak, Kajetan Szamotuła, Dawid Celian

## Dlaczego: 

Celem systemu jest podlewanie czy coś.
Oprogramowanie jest przeznaczone dla ogrodników potrzebujących sterownika na podstawie rutyn podlewania ustalonych przez użytkownika. 
Ten User Guide obejmuje instalację programu, ustalenie własnych sekcji do podlewania oraz działanie z oprawą webową. 

## Funkcjonalności: 
Główną funkcją systemu jest podlewanie kontrolowane automatycznie. Użytkownik może sterować: 
    godziną rozpoczęcia podlewania, 
    per sekcja czas albo ilość wody do użycia, 
    w które dni tygodnia ma podlewać, 

Jest tylko możliwość kontrolowania planowanych podlewań przez lokalą stronę internetową. 

## Wymagania: 
    Wymagane do korzystania:
    * Raspbeperry Pi(0.5 GB RAMu, albo więcej)
    * Elektrozawory(tyle to chce się sekcji) 
    * Przekazniki(przynajmniej tyle co sekcji) np. [link](https://botland.com.pl/przekazniki-przekazniki-arduino/6940-modul-przekaznikow-16-kanalow-z-optoizolacja-styki-10a250vac-cewka-5v-5904422359911.html)
    * Wodomierz na sensor Halla. np. [link](https://botland.com.pl/czujniki-przeplywu/8896-czujnik-przeplywu-cieczy-yf-s201-30lm-gwint-12--5904422366933.html)
    * Przy tym sprzęcie co powyżej jeszcze takie coś się przyda: [link](https://botland.com.pl/konwertery-napiec/8590-konwerter-poziomow-logicznych-dwukierunkowy-8-kanalowy-5904422336660.html) (bo Raspberry Pi ma sygnał 3.3V a te przekazniki chcą 5V)  
    * Oczywiście też jakiś sprzęt wodny do rozprowadzania wody. 
    * Konieczne są też zdolności spięcia tego wszystkiego. 
 !!Dlaczego to jest w code blocku??

## Instalacja i konfiguracja: 

 

### instalacja na Raspberry Pi 

 

#### Instalacja Dockera uzywajac convinience script 

 

```bash 

Sudo apt update 

Sudo apt install -y git curl 

curl -fsSL https://get.docker.com -o get-docker.sh 

sh get-docker.sh 

sudo usermod -aG sudo $USER 

sudo reboot now 

``` 

 

#### Wstepna konfiguracja programu 

 

```bash 

git clone https://github.com/BreadAlloy/system-podlewania-ogrodu.git 

cd system-podlewania-ogrodu 

sudo chmod +x database_init.sh 

sudo chmod +x manage.sh 

./database_init.sh 

``` 

 

#### Uruchamianie 

 

Z folderu projektu 

 

```bash 

Docker compose up -d --build 

``` 

 

#### Zatrzymywanie 

 

Z folderu projektu 

 

```bash 

Docker compose down 

``` 

 

#### Zatrzymywanie z usuwaniem 

 

Z folderu projektu 

 

```bash 

Docker compose down -v 

Cd .. 

Sudo Rm -rf system-podlewania-ogrodu 

``` 

### Rezultat konfiguracji:
Nasze oprogramowanie hostuje strony: 

* http://{ip_raspberry}/logi:8000 (do wglądu w historie tego co się wydarzyło)

* http://{ip_raspberry}:8000 (do ustalania planów podlewania) 

## Rozwiązywanie problemów:
Do spróbowania:
    * Restart 
    * Plik logi.txt jest za duży(można go zkasować wtedy po prostu) 
    Kontakt z zespołem: [link](https://github.com/BreadAlloy/system-podlewania-ogrodu/issues)

 

Link do repozytorium: [link](https://github.com/BreadAlloy/system-podlewania-ogrodu)
