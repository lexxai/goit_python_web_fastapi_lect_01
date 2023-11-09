

## AUTH
### HTTPBearer, HTTPAuthorizationCredentials
- signup:
![auth-03](doc/auth-03.png)

- get_token/login by json:
![auth-02](doc/auth-02.png)

- access with token:
![auth-01](doc/auth-01.png)

- get_token/login by oauth2 form:
![auth-02](doc/auth-04.png)

- get_token/login by oauth2 form:
![auth-02](doc/auth-05.png)

- get_token/login by oauth2 form:
![auth-02](doc/auth-06.png)

- access with token:
![auth-02](doc/auth-07.png)





## DOCKER
### .env
```
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=XXXXXXX
POSTGRES_HOST=pg,localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi
TOKEN_SECRET_KEY="some secret"
```

### RUN
docker-compose up -d code 