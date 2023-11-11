@echo off
PUSHD ..\goit_python_web_fastapi_lect_01

alembic init migrations

alembic revision --autogenerate -m "Init"

POPD