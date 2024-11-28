from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.orm import relationship

from .database import Base
#table des attacks
class Attack(Base):
    __tablename__ = 'attacks'

    id = Column(Integer, primary_key=True,autoincrement = True, index=True)

    caseNumber = Column(String, nullable = True)
    date = Column(String, nullable=True)
    year = Column(String, nullable=True)
    type = Column(String, nullable=True)
    country = Column(String, nullable=True)
    area = Column(String, nullable=True)
    location = Column(String, nullable=True)
    activity = Column(String, nullable=True)
    name = Column(String, nullable=True)
    sex = Column(String, nullable=True)
    age = Column(String, nullable=True)
    injury = Column(String, nullable=True)
    fatal = Column(String, nullable=True)
    time = Column(String, nullable=True)
    species = Column(String, nullable=True)
    investigator_or_source = Column(String, nullable=True)
    pdf = Column(String, nullable=True)
    href_formula = Column(String, nullable=True)
    href = Column(String, nullable=True)
    original_order = Column(String, nullable=True)  

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="attacks")
    

