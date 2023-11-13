import time
from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from sqlalchemy import text
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.routes import cats, owners
from src.routes.auth import auth
# from src.routes.auth import auth_simple, auth_oauth2, auth_oauth2refresh, 
from src.conf.auth import AUTH_LIB


app = FastAPI()

origins = [ 
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")





@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["X-PERF"] = str(duration)
    return response


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "tilte": "Cats APP"}
    )


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
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
