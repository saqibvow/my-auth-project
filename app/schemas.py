from fastapi import FastAPI,Depends
from pydantic import BaseModel,EmailStr, model_validator
from pwdlib import PasswordHash
from sqlmodel import Field, Session, SQLModel, create_engine, select 
from typing import Annotated
from pydantic_core import PydanticCustomError


app = FastAPI()
password_hasher = PasswordHash.recommended()

class User_Registration(BaseModel):
    full_name: str
    email_addr: EmailStr
    password: str
    conf_password: str = Field(exclude=True)
    @model_validator(mode='after')
    def check_pass_match(self):
        if self.password != self.conf_password:
            print("PASSWORD MISMATCH !!!")
            raise PydanticCustomError(
                'password mismatch',
                'write  again your password',
            )
        
        return self

class Hero_Db(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str | None = Field(index=True)
    email_addr: str | None = Field(index=True)
    password: str 



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
def create_hero(hero:User_Registration, session: SessionDep):
    filtered_data = hero.model_dump(exclude={"conf_password"})
    filtered_data["password"] = password_hasher.hash(filtered_data["password"])
    db_user = Hero_Db(**filtered_data)
    print(filtered_data["password"])
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user



