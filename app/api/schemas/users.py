from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated

#Schéma pour la table user

class User(BaseModel):
    firstName: str
    password: str
    
class UserCreate(User):
    pass

class UserInDB(User):
    id: int
    attacks: Optional[List[str]] = []

    class Config:
        orm_mode = True