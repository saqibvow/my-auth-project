from fastapi import FastAPI
from pydantic import BaseModel,EmailStr, model_validator
from pwdlib import PasswordHash

app = FastAPI()

class user_registration(BaseModel):
    FUll_NAME: str
    EMAIL_ADDR: EmailStr
    PASSWORD: str
    CONF_PASSWORD: str
    @model_validator(mode='after')
    def check_pass_match(self):
        if self.PASSWORD != self.CONF_PASSWORD:
            raise ValueError('Password  do not match')
        return self
    password_hash = PasswordHash.recommended()
    hash = password_hash.hash(PASSWORD)