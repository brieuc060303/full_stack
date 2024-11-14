from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

#table des users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    password = Column(String, index=True)
    attacks = relationship("Attack", back_populates="user")