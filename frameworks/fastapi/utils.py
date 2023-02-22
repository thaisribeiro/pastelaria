SETTINGS='''from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):
    NAME_APP: str = config("NAME_APP")
    HOST: str = config("HOST")
    PORT: int = config("PORT")
    DATABASE_HOST: str = config("DATABASE_HOST")
    NAME_DATABASE: str = config("NAME_DATABASE")

settings = Settings()
'''

INIT_ROUTER='''from fastapi import APIRouter
from api.routers import user

api_routers = APIRouter()

api_routers.include_router(user.router)
'''

README = '''#### 🤖 Este readme foi gerado pela Pastelaria
This is a boilerplate using the fastAPI framework

# Installation

create a virtual environment

``` shell
virtualenv venv --python=3.10
```
activate the virtual environment

```shell
source venv/bin/activate
```
# Dependencies

Use `pip` to download project dependencies:

```shell
pip install -r requirements.txt
```
# Settings

Configure environments in `.env`

# Execution
 Run
```shell
uvicorn main:app --reload
```
# Routes 
url: http://localhost:8000/docs
'''

ENV = '''NAME_APP='nome_do_app'
HOST='127.0.0.1:8000'
PORT='8000'
DATABASE_HOST='host'
NAME_DATABASE='nome_database'
'''
MAIN_UTIL='''import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title='nome_app')

class User(BaseModel):
    name: str
    address: str
    email: str
    

users = []

@app.post("/users")
async def create_user(user: User):
    users.append(user.dict())
    return users
        
if __name__ == "__main__":
    uvicorn.main(app, reload=True)


'''