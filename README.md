

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

- get_token/login by oauth2 form with refresh:
![auth-02](doc/auth-08.png)

- token refresh saved to Database:
![auth-02](doc/auth-09.png)

- decoded refresh token:
![auth-02](doc/auth-10.png)

- token refresh by refresh_token:
![auth-02](doc/auth-11.png)

- decoded new refresh token:
![auth-02](doc/auth-12.png)


## REAUTH BY REFRESH_TOKEN in COOKIES
Define cookie for refresh_token
![auth-cookies](doc/auth-13-cookies.png)

Auth using a refresh_token (cookie) sicne access_token has expired and get a new access_token, and the client side should save and use its new new_access_token as the next access_token
![auth show new token](doc/auth-14-new_a_token.png)

Next auth with use new access_token as access_token
![auth with new token](doc/auth-15-use_new_a_token.png)

## REAUTH BY REFRESH_TOKEN in DATABSE
Auth using a refresh_token (cookie) sicne access_token has expired and get a new access_token, and the client side should save and use its new new_access_token as the next access_token
![auth show new token](doc/auth-14-new_a_token.png)




## DOCKER
### .env
```
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=XXXXXXX
POSTGRES_HOST=pg,localhost
POSTGRES_PORT=5432
POSTGRES_DB=fastapi
TOKEN_SECRET_KEY="some secret"
AUTH_LIB=OAuth2
```

### RUN
docker-compose up -d code 