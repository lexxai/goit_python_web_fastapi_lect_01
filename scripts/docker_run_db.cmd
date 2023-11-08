@echo off

docker start pg_fastapi
docker run --name pg_fastapi -p 5432:5432 --env-file ../.env -d postgres


   

