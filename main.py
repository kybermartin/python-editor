import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import requests

# -----------------------
# Configuration
# -----------------------
PORT = int(os.getenv("PORT", 10000))

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scripts.db")
# Render may provide DATABASE_URL that starts with postgres:// — SQLAlchemy expects postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Optional: restrict CORS by setting FRONTEND_URL env var (comma-separated list)
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
allowed_origins = [o.strip() for o in FRONTEND_URL.split(",")] if FRONTEND_URL != "*" else ["*"]

# Judge0 config
JUDGE0_URL = "https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=false&wait=true"
JUDGE0_KEY = os.getenv("JUDGE0_API_KEY", "")
HEADERS = {
    "x-rapidapi-key": JUDGE0_KEY,
    "x-rapidapi-host": "judge0-ce.p.rapidapi.com"
}

# -----------------------
# Database setup
# -----------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    scripts = relationship("Script", back_populates="owner")

class Script(Base):
    __tablename__ = "scripts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    code = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="scripts")

Base.metadata.create_all(bind=engine)

# -----------------------
# FastAPI app
# -----------------------
app = FastAPI(title="Python Editor Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

class ScriptRequest(BaseModel):
    title: str
    code: str
    user_name: str

@app.get("/")
def root():
    return {"message": "Python editor backend running."}

@app.post("/run")
def run_code(req: CodeRequest):
    if not JUDGE0_KEY:
        raise HTTPException(status_code=500, detail="Judge0 API key not set (JUDGE0_API_KEY).")
    payload = {"language_id": 71, "source_code": req.code, "stdin": ""}
    response = requests.post(JUDGE0_URL, json=payload, headers=HEADERS, timeout=30)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Judge0 error: {response.status_code}")
    return response.json()

@app.post("/save")
def save_script(data: ScriptRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.name == data.user_name).first()
    if not user:
        user = User(name=data.user_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    script = Script(title=data.title, code=data.code, owner_id=user.id)
    db.add(script)
    db.commit()
    return {"message": "Skript uložený"}

@app.get("/scripts/{username}")
def get_scripts(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.name == username).first()
    if not user:
        return []
    scripts = db.query(Script).filter(Script.owner_id == user.id).all()
    return [{"title": s.title, "code": s.code} for s in scripts]
