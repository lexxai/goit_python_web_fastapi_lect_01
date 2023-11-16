

## AUTH
### HTTPBearer, HTTPAuthorizationCredentials
- signup:
![auth-03](doc/auth-03.png)

- get_token/login by json:
![auth-02](doc/auth-02.png)

- access with token:
![auth-01](doc/auth-01.png)

### OAuth2

- get_token/login by oauth2 form:
![auth-02](doc/auth-04.png)

- get_token/login by oauth2 form:
![auth-02](doc/auth-05.png)

- get_token/login by oauth2 form:
![auth-02](doc/auth-06.png)

- access with token:
![auth-02](doc/auth-07.png)

### OAuth2 + refresh

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

Auth using a refresh_token (cookie) and check on saved DB, sicne access_token has expired and get a new access_token, and the client side should save and use its new new_access_token as the next access_token
![auth show new token](doc/auth-16-chek_token_db.png)

### USE REFRESH_TOKEN in COOKIES + REFRESH_TOKEN IN DB 

Set changed in DB
![auth show new token](doc/auth-17-token_db-other.png)

Now rigth refresh_token by sign not aceeped, since not same as DB
![auth show new token](doc/auth-18-token_db-other-deny.png)

After wrong refresh_token used, refresh_token in DB cleared
![auth show new token](doc/auth-19-token_db-cleared.png)


### GRAVATAR LINK
![auth GRAVATAR](doc/auth-20-gravatar.png)


## JavaSript Client
### Login
![login](doc/js-clien-01-login.png)

### Auth token local storage
![ Auth token local storage](doc/js-clien-03-token-storage.png)

### List cats and owners
![List cats and owners](doc/js-clien-02-list.png)

## Owner create
![Owner create](doc/js-clien-04-form.png)

## Client Js FastAPI Static
### Index
![index](doc/static-client-01.png)
### Login
![index](doc/static-client-02.png)
### List 
![index](doc/static-client-03.png)
### Docs
![index](doc/static-client-04.png)

## Client Js FETCH ERROR AND REFRESH TOKEN
### First success REFRESH TOKEN and relaod data of cats
![index](doc/static-client-05-reauth.png)

### Limit of bad try REFRESH TOKEN by calling himself and redirect to login page if fail.
![index](doc/static-client-06-try-bad-reauth.png)


## SEND EMAIL
### API
![index](doc/email-01.png)
### WEBMAIL
![index](doc/email-02.png)
### Sign up
![index](doc/email-02a.png)
### WEBMAIL Confirmation email
![index](doc/email-02b.png)
### Click confirm link
![index](doc/email-03.png)
### User on database changed filed confirmed
![index](doc/email-04.png)
### User login deny before confirm by link
![index](doc/email-05.png)
### User login allowed after confirm by link
![index](doc/email-06.png)



## Redis cache SQL 
### Save to redis
![save redis](doc/redis-02.png)
### Get from redis
![get redis](doc/redis-01.png)

## DOCKER
### .env
example: doc\dot.env-example

### RUN
docker-compose up -d code 

### INSPECT HEALTH
- docker ps
- docker ps  -f name=web_fastapi-code-1
```
CONTAINER ID   IMAGE                       COMMAND                 CREATED          STATUS                      PORTS                    NAMES
a5bfb08fe7a8   lexxai/web_fastapi:latest   "/bin/sh -c ./run.sh"   13 minutes ago   Up 13 minutes (unhealthy)   0.0.0.0:9000->9000/tcp   web_fastapi-code-1  
```
- docker inspect --format='{{json .State.Health}}'  web_fastapi-code-1 