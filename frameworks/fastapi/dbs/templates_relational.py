DATABASE='''from api.config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = settings.DATABASE_HOST

db_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base = declarative_base()

def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
'''

MAIN='''import uvicorn
import api.models.user as models

from fastapi import FastAPI
from api.routers import api_routers
from api.config.settings import settings
from api.server.database import db_engine

app = FastAPI(title=settings.NAME_APP)

models.Base.metadata.create_all(bind=db_engine)

# add routers
app.include_router(api_routers)
        
if __name__ == "__main__":
    uvicorn.main(app, host=settings.HOST, port=settings.PORT, reload=True)
'''

ROUTER = '''from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from api.schemas.user import UserSchemaBase, UserSchemaList
from api.server.database import get_db
from api.repositories.user import create_user, list_users, list_user, update_user, delete_user

router = APIRouter(tags=["Users"], prefix="/users")

@router.post("", response_model=UserSchemaBase, status_code=201)
async def add_user(user: UserSchemaBase, db: Session = Depends(get_db)):
    user =  await create_user(db, user)
    return user

@router.get("", response_model=List[UserSchemaList], status_code=200)
def get_users(skip: int = 1, limit: int = 100, db: Session = Depends(get_db)):
    return list_users(db, skip, limit)

@router.get("/{user_id}", response_model=UserSchemaList, status_code=200)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = list_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@router.put("/{user_id}", response_model=UserSchemaList, status_code=200)
async def modify_user(user_id: int, user: UserSchemaBase, db: Session = Depends(get_db)):
    user = await update_user(db, user_id, user)
    return user

@router.delete("/{user_id}", status_code=200)
async def deleted_user(user_id: int, db: Session = Depends(get_db)):
    await delete_user(db, user_id)
    return "User deleted successfully"
'''

SCHEMA = '''from typing import Optional
from pydantic import BaseModel, EmailStr

class UserSchemaBase(BaseModel):
    name: str
    address: str
    email: EmailStr
    
    class Config:
        orm_mode = True # allows the app to take ORM objects and translate them into responses automatically
        schema_extra = {
            "example": {
                "name": "John Doe",
                "address": "R dos Blocos, 10",
                "email": "jdoe@x.edu.ng"
            }
                
        }

class UserSchemaUpdate(BaseModel):
    name: Optional[str]
    address: Optional[str]
    email: Optional[EmailStr]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "John Doe",
                "address": "R dos Blocos, 10",
                "email": "jdoe@x.edu.ng"
            }
        }

class UserSchemaList(UserSchemaBase):
    id: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "1",
                "name": "John Doe",
                "address": "R dos Blocos, 10",
                "email": "jdoe@x.edu.ng"
            }
        }
'''

REPOSITORY='''from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.models.user import User
from api.schemas.user import UserSchemaBase, UserSchemaUpdate

async def create_user(db: Session, user: UserSchemaBase):
    try:
        user = user if type(user) == dict else user.dict()
        user = User(name=user['name'], address=user['address'], email=user['email'])
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def list_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        users = db.query(User).offset(skip).limit(limit).all()
        return users
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

def list_user(db: Session, user_id):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def update_user(db: Session, user_id, user: UserSchemaUpdate):
    try:
        db_user_id = list_user(db, user_id)
        if db_user_id:
            update_user_encoded = jsonable_encoder(user)
            db_user_id.name = update_user_encoded.get('name', db_user_id.name)
            db_user_id.address = update_user_encoded.get('address', db_user_id.address)
            db_user_id.email = update_user_encoded.get('email', db_user_id.email)
            updated_user = db.merge(db_user_id)
            db.commit()
            return updated_user
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
async def delete_user(db: Session, user_id):
    try:
        db_user = db.query(User).filter_by(id=user_id).first()
        db.delete(db_user)
        db.commit()
    except Exception: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
'''

MODELS='''from sqlalchemy import Column, Integer, String
from api.server.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    address = Column(String(255))
    email = Column(String(255), index=True)
    
    def __repr__(self):
        return 'UserModel(name=%s, address=%s, email=%s)' % (self.name, self.address, self.email)
    
'''

REQUIREMENTS = '''fastapi==0.92.0
fastapi-mail==1.2.5
uvicorn==0.20.0
pydantic==1.10.5
python-decouple==3.7
SQLAlchemy==2.0.4
'''