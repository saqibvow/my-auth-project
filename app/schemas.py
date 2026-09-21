from fastapi import FastAPI,Depends
from pydantic import BaseModel,EmailStr, model_validator
from pwdlib import PasswordHash
from sqlmodel import Field, Session, SQLModel, create_engine, select 
from typing import Annotated


app = FastAPI()

class User_Registration(BaseModel):
    full_name: str
    email_addr: EmailStr
    password: str
    conf_password: str
    @model_validator(mode='after')
    def check_pass_match(self):
        if self.password != self.conf_password:
            raise ValueError('Password  do not match')
        return self

class Hero_Db(SQLModel, table=True):
    id: int | None = Field(default=None , primary_key=True)
    full_name: str | None = Field(index=True)
    email_addr: str | None = Field(index=True)
    password: str


class User_Response(BaseModel):

    full_name: str

    email_addr: EmailStr

mysql_url = "mysql+pymysql://root:iamsaqib__1@localhost:3306/my_auth_db"
engine = create_engine(mysql_url, echo=True)
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/")
def create_hero(hero: Hero_Db, session: SessionDep) -> User_Response:
    db_user = Hero_Db(
    full_name=hero.full_name,          
    email_addr=hero.email_addr,   
    password=hero.password, 
)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user



