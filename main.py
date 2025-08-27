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

# class Jwt(Base):
#     __tablename__="jwt"
#     id = Column(Integer, primary_key=True)
#     username =  Column(String, nullable=False)
#     jwt = Column(String, nullable=False)
#     user_id = Column(Integer,nullable=False)



engine = create_engine("sqlite:///local.db", echo=True)

SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
from contextlib import contextmanager
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user():
    db_generator = get_db()
    db = next(db_generator)
    limit = 100
    offset = 0

    while True:
        payload = {
            "limit":limit,
            "offset": offset
        }
        response = requests.get('http://2.179.194.90/user_data/',params=payload)
        offset += 100
        try:
            users_to_add = [
                User(
                    username=user_data.get("username"),
                    password=user_data.get("password"),
                    user_id=user_data.get("user_id")
                )
                for user_data in response.json()
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

if __name__ == "__main__":
    save_user()