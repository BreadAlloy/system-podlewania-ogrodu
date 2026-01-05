# system-podlewania-ogrodu

## PLZ FIX

Aplikacja włączana na dockerze łączy sie z gpio_workerem, gdy ZaworyView jest getowany. Ta operacja w tym momencie kończy się to errorem "ConnectionRefusedError". Moja teoria jest taka, że nie widzi socketa serwera przez Dockera. Gdy zadziała to gpio-worker powinien printnać "dziala :)". Socket jest na porcie z konfigu: config.port_do_komunikacji. Kod jest lepiony, nie oceniać.

