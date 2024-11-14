from .database import SessionLocal
#Accéder a la base de donnée
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
