from sqlalchemy.orm import Session
from backend import schemas
from backend import models


class CRUDFitbitToken:
    def get(self, db: Session, session_id: str):
        return db.query(models.FitbitToken).get(session_id)

    def create(self, db: Session, obj: schemas.TokenCreate):
        db_obj = models.FitbitToken(
            session_id=obj.session_id
            # WIP
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, session_id: str):
        db.query(models.FitbitToken).filter(
            session_id == models.FitbitToken.session_id
        ).delete()
        db.commit()
        db.refresh()
        return session_id


crud_fitbit_token = CRUDFitbitToken()
