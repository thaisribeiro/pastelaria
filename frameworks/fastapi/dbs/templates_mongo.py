DATABASE = '''from api.config.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None
    user_db = None
    
db = Database()

async def connect_db():
    db.client = AsyncIOMotorClient(settings.DATABASE_HOST, maxPoolSize=10, minPoolSize=10)
    db.user_db = db.client[settings.NAME_DATABASE].user

async def close_conn_db():
    db.client.close()
'''

MAIN = '''import uvicorn
from fastapi import FastAPI
from api.routers import api_routers
from api.config.settings import settings
from api.server.database import connect_db, close_conn_db

app = FastAPI(title=settings.NAME_APP)

# add connection database
app.add_event_handler("startup", connect_db)
app.add_event_handler('shutdown', close_conn_db)

# add routers
app.include_router(api_routers)
        
if __name__ == "__main__":
    uvicorn.main(app, host=settings.HOST, port=settings.PORT, reload=True)

'''

ROUTER = '''from fastapi import APIRouter
from typing import List
from api.schemas.user import UserSchemaBase, UserSchemaUpdate
from api.repositories.user import create_user, list_user, list_users, update_user, delete_user

router = APIRouter(tags=["User"], prefix="/user")

@router.post("", status_code=201)
async def add_user(user: UserSchemaBase):
    user = await create_user(user)
    return user
    
@router.get("", status_code=200)
async def get_users(skip: int, limit: int):
    users = await list_users(skip, limit)
    return users

@router.get("/{user_id}", status_code=200)
async def get_user(user_id: str):
    user = await list_user(user_id)
    return user

@router.put("/{user_id}", status_code=200)
async def modify_user(user_id: str, user: UserSchemaUpdate):
    user = await update_user(user_id, user)
    return user

@router.delete("/{user_id}", status_code=200)
async def deleted_user(user_id):
    await delete_user(user_id)
    return "User deleted successfully"
'''

SCHEMA = '''from typing import Optional
from pydantic import BaseModel, EmailStr

class UserSchemaBase(BaseModel):
    name: str
    address: str
    email: EmailStr
    
    class Config:
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
        schema_extra = {
            "example": {
                "name": "John Doe",
                "address": "R dos Blocos, 10",
                "email": "jdoe@x.edu.ng"
            }
        }
'''

REPOSITORY = '''from fastapi import HTTPException, status
from bson.objectid import ObjectId
from api.server.database import db
from api.schemas.user import UserSchemaBase, UserSchemaUpdate

async def create_user(user: UserSchemaBase):
    try:
        user = user if type(user) == dict else user.dict()
        user = await db.user_db.insert_one(user)
        
        if user.inserted_id:
            return await list_user(user.inserted_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
async def list_users(skip: int=0, limit: int=100):
    try:
        users_cursor = db.user_db.find().skip(int(skip)).limit(int(limit))
        users = await users_cursor.to_list(length=int(limit))
        return list(map(fix_user_id, users))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def list_user(user_id):
    try:
        user = await _get_user_or_404(user_id)
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        
async def update_user(user_id, user_data: UserSchemaUpdate):
    try:
        user = user_data if type(user_data) == dict else user_data.dict()
        user = {k: v for k, v in user.items() if v is not None}
        user_op = await db.user_db.update_one({"_id": validate_object_id(user_id)}, {"$set": user})
        
        if user_op.modified_count:
            return await _get_user_or_404(user_id)
        
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def delete_user(user_id):
    try:
        await _get_user_or_404(user_id)
        user = await db.user_db.delete_one({"_id": validate_object_id(user_id)})
        
        if user.deleted_count:
            return {"status": "deleted product"}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

async def _get_user_or_404(id):
    user = await db.user_db.find_one({"_id": validate_object_id(id)})
    if user:
        return fix_user_id(user)
    
    raise HTTPException(status_code=404, detail="User not found")

def fix_user_id(user):
    if user.get("_id", False):
        user["_id"] = str(user["_id"])
        return user
    
    raise ValueError("No _id found")

def validate_object_id(id):
    try:
        _id = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid id")
    
    return _id
'''
REQUIREMENTS = '''fastapi==0.92.0
fastapi-mail==1.2.5
uvicorn==0.20.0
pydantic==1.10.5
python-decouple==3.7
motor==3.1.1
'''