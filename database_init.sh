docker compose build

echo running makemigrations
./manage.sh makemigrations

echo running migrate
./manage.sh migrate

echo running transfer_zawory
./manage.sh transfer_zawory