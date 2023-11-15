@echo off

PUSHD ..
docker compose  --env-file .env --file docker-compose-db.yml  up -d 
POPD

   

