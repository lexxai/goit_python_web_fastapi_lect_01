@echo off

PUSHD ..\goit_python_web_fastapi_lect_01

alembic revision --autogenerate -m "Updates"
alembic upgrade head 

POPD