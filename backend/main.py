from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional, List
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "saas-analytics-secret-key-change-me-12345")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./saas_analytics.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(
    title="SaaS Analytics Dashboard API",
    description="Track MRR, Churn, Revenue and Subscriptions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== MODELS ====================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    company_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    subscriptions = relationship("Subscription", back_populates="owner")

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    customer_email = Column(String)
    plan_name = Column(String)  # Starter, Pro, Enterprise
    amount = Column(Float)  # monthly amount
    status = Column(String, default="active")  # active, cancelled, past_due
    start_date = Column(DateTime, default=datetime.utcnow)
    cancelled_at = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="subscriptions")

Base.metadata.create_all(bind=engine)

# ==================== SCHEMAS ====================
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    company_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    company_name: Optional[str]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

class SubscriptionCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    plan_name: str
    amount: float

class SubscriptionOut(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    plan_name: str
    amount: float
    status: str
    start_date: datetime
    cancelled_at: Optional[datetime]

    class Config:
        from_attributes = True

class AnalyticsSummary(BaseModel):
    mrr: float
    total_revenue: float
    active_subscribers: int
    churned_this_month: int
    churn_rate: float
    total_subscriptions: int

# ==================== UTILS ====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# ==================== AUTH ====================
@app.post("/auth/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        company_name=user.company_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": user}

@app.get("/auth/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user

# ==================== SUBSCRIPTIONS ====================
@app.post("/subscriptions", response_model=SubscriptionOut)
def create_subscription(data: SubscriptionCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sub = Subscription(**data.dict(), owner_id=current_user.id)
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub

@app.get("/subscriptions", response_model=List[SubscriptionOut])
def list_subscriptions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Subscription).filter(Subscription.owner_id == current_user.id).order_by(Subscription.start_date.desc()).all()

@app.patch("/subscriptions/{sub_id}/cancel")
def cancel_subscription(sub_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter(Subscription.id == sub_id, Subscription.owner_id == current_user.id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Subscription not found")
    sub.status = "cancelled"
    sub.cancelled_at = datetime.utcnow()
    db.commit()
    return {"message": "Subscription cancelled", "id": sub_id}

# ==================== ANALYTICS ====================
@app.get("/analytics/summary", response_model=AnalyticsSummary)
def get_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    subs = db.query(Subscription).filter(Subscription.owner_id == current_user.id).all()

    active = [s for s in subs if s.status == "active"]
    cancelled = [s for s in subs if s.status == "cancelled"]

    mrr = sum(s.amount for s in active)
    total_revenue = sum(s.amount for s in subs)  # simplified

    # Simple churn calculation (this month)
    now = datetime.utcnow()
    churned_this_month = len([
        s for s in cancelled
        if s.cancelled_at and s.cancelled_at.month == now.month and s.cancelled_at.year == now.year
    ])

    total_ever = len(subs) or 1
    churn_rate = round((len(cancelled) / total_ever) * 100, 2)

    return AnalyticsSummary(
        mrr=round(mrr, 2),
        total_revenue=round(total_revenue, 2),
        active_subscribers=len(active),
        churned_this_month=churned_this_month,
        churn_rate=churn_rate,
        total_subscriptions=len(subs)
    )

@app.get("/")
def root():
    return {
        "message": "SaaS Analytics Dashboard API is running 📊",
        "docs": "/docs",
        "author": "Rajiv Kapur"
    }
