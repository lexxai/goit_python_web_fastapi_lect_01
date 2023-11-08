import time
from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


from sqlalchemy import text
from sqlalchemy.orm import Session


from src.database.db import get_db
from src.routes import cats, owners
from src.auth.authSimple import Hash, create_access_token, get_current_user
from src.shemas import UserModel
from src.database.models import User


app = FastAPI()

hash_handler = Hash()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

PUBLIC_APP = True


@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start_time
    response.headers["X-PERF"] = str(duration)
    return response


@app.post("/signup")
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = db.query(User).filter(User.email == body.username).first()
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
        )
    new_user = User(
        email=body.username, password=hash_handler.get_password_hash(body.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"new_user": new_user.email}


@app.post("/login")
async def login(body: UserModel, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email" if PUBLIC_APP else "Invalid credentianal",
        )
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password" if PUBLIC_APP else "Invalid credentianal",
        )
    # Generate JWT
    access_token = await create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/secret")
async def read_item(current_user: User = Depends(get_current_user)):
    return {"message": "secret router", "owner": current_user.email}


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


app.include_router(owners.router, prefix="/api")
app.include_router(cats.router, prefix="/api")


print("MAIN", __name__)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
