PUSHD ..\goit_python_web_fastapi_lect_01

taskkill /IM "uvicorn.exe" /F
uvicorn main:app --reload --port 9000
taskkill /IM "uvicorn.exe" /F
POPD