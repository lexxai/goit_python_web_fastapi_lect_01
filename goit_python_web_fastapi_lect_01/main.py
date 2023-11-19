from contextlib import asynccontextmanager
import re
import time
from ipaddress import ip_address
from typing import Callable

from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import text
from sqlalchemy.orm import Session
import redis.asyncio as redis
import uvicorn


from src.database.db import get_db
from src.routes import cats, owners
from src.routes.auth import auth

# from src.routes.auth import auth_simple, auth_oauth2, auth_oauth2refresh,
# from src.conf.auth import AUTH_LIB
from src.conf.config import settings


async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)
    print("startup done")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("lifespan before")
    await startup()
    yield
    print("lifespan after")


app = FastAPI(lifespan=lifespan)  # type: ignore

origins = ["http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

user_agent_ban_list = [r"Gecko", r"Python-urllib"]
@app.middleware("http")
async def user_agent_ban_middleware(request: Request, call_next: Callable):
    user_agent = request.headers.get("user-agent")
    for ban_pattern in user_agent_ban_list:
        if re.search(ban_pattern, user_agent): # type: ignore
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
    response = await call_next(request)
    return response


# @app.on_event("startup")
ALLOWED_IPS = [ip_address('192.168.1.0'), ip_address('172.16.0.0'), ip_address("127.0.0.1")]

@app.middleware("http")
async def limit_access_by_ip(request: Request, call_next: Callable):
    ip = ip_address(request.client.host)
    if ip not in ALLOWED_IPS:
        return JSONResponse(status_code=status.HTTP_402_PAYMENT_REQUIRED, content={"detail": "Not allowed IP address"})
    response = await call_next(request)
    return response




# banned_ips = [ip_address("192.168.1.1"), ip_address("192.168.1.2"), ip_address("127.0.0.2")]

# @app.middleware("http")
# async def ban_ips(request: Request, call_next: Callable):
#     ip = ip_address(request.client.host)
#     if ip in banned_ips:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["X-PERF"] = str(duration)
    return response


@app.get(
    "/",
    response_class=HTMLResponse,
    description="No more than 2 requests per 5 seconds",
    dependencies=[Depends(RateLimiter(times=2, seconds=5))],
)
# @app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "tilte": "Cats APP"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


# print(f"{AUTH_LIB=}")
# if AUTH_LIB == "Simple":
#     app.include_router(auth_simple.router, prefix="/api/auth")
# elif AUTH_LIB == "OAuth2REfresh":
#     app.include_router(auth_oauth2refresh.router, prefix="/api/auth")
# else:
#     app.include_router(auth_oauth2.router, prefix="/api/auth")

app.include_router(auth.router, prefix="/api/auth")

app.include_router(owners.router, prefix="/api")
app.include_router(cats.router, prefix="/api")


# print("MAIN", __name__)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
