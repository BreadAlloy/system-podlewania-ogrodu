#!/usr/bin/bash
docker compose run -w /usr/src/app/ --rm web "$@"