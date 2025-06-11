from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime, timedelta
from backend.utils import hash_password  # Import de la fonction de hachage
DATABASE_URL = "postgres://u6005n94db2o7c:p55ef39aee90a31aceba35f982e8686bbe6bd747f9bc724eab94b245d60c191e8@c4uljrch9k8rpm.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/deav32kecbfima"

# Connexion PostgreSQL (Remplace avec ton URL Heroku)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

class User(Base):
    __tablename__ = "userscae"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Haché avec bcrypt
    is_subscribed = Column(Boolean, default=False)
    trial_end_date = Column(DateTime, default=datetime.utcnow() + timedelta(days=3))  # Essai 3 jours

    # ✅ Add new fields
    name = Column(String, nullable=True)  
    licence = Column(String, nullable=True)  
    customer_stripe_id = Column(String, nullable=True)  # Stripe Customer ID


# Création des tables
#def init_db():
#    Base.metadata.create_all(bind=engine)




# ✅ Function to check if a user already exists
def check_user_existence(email: str) -> bool:
    """Check if a user with the given email exists in the database."""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first() is not None
    finally:
        db.close()

# ✅ Function to add a new user
def add_user(name: str, email: str, password: str, trial_end_date: str, licence: str):
    """Add a new user to the database."""
    db = SessionLocal()
    try:
        new_user = User(
            name=name,
            email=email,
            password=password,
            trial_end_date=trial_end_date,
            licence=licence,
            is_subscribed=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    finally:
        db.close()
        
        
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

