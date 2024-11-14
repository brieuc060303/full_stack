from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import uuid4
from typing_extensions import Annotated, Optional
        
#Schéma pour la table attacks

class Attack(BaseModel):
    caseNumber: Optional[str] = None
    date: Optional[str] = None
    year: Optional[str] = None
    type: Optional[str] = None
    country: Optional[str] = None
    area: Optional[str] = None
    location: Optional[str] = None
    activity: Optional[str] = None
    name: Optional[str] = None
    sex: Optional[str] = None
    age: Optional[str] = None
    injury: Optional[str] = None
    fatal: Optional[str] = None
    time: Optional[str] = None
    species: Optional[str] = None
    investigator_or_source: Optional[str] = None
    pdf: Optional[str] = None
    href_formula: Optional[str] = None
    href: Optional[str] = None
    original_order: Optional[str] = None


class AttackCreate(Attack):
    pass

class AttackInDB(Attack):
    caseNumber: int

    class Config:
        orm_mode = True
        
class AttackUpdate(Attack):
    pass