# db_sync.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    user_id =  Column(Integer,nullable=False)

engine = create_engine("sqlite:///local.db", echo=True)

SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)



