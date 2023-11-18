@echo off

PUSHD ..
docker compose  --env-file .env-prod --file docker-compose-db.yml  up -d 
POPD

   

