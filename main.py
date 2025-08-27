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

class Jwt(Base):
    __tablename__="jwt"
    id = Column(Integer, primary_key=True)
    username =  Column(String, nullable=False)
    jwt = Column(String, nullable=False)
    user_id = Column(Integer,nullable=False)



engine = create_engine("sqlite:///local.db", echo=True)

SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user(users_list: dict):
    db_generator = get_db()
    db = next(db_generator)
    
    try:
        users_to_add = [
            User(
                username=user_data.get("username"),
                password=user_data.get("password"),
                user_id=user_data.get("user_id")
            )
            for user_data in users_list
        ]
        
        # تمام اشیاء را به صورت یکجا به Session اضافه کنید
        db.add_all(users_to_add)
        
        db.commit()
        print("All users saved successfully in a single batch!")
        
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()