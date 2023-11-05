@echo off

docker run --name pg_fastapi -p 5432:5432 --env-file ../.env -d postgres


                    

