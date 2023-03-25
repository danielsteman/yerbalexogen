from typing import Optional
from sqlalchemy.orm import Session
from backend import schemas
from backend import models


class CRUDFitbitToken:
    def get(self, db: Session, session_id: str) -> Optional[models.FitbitToken]:
        return db.query(models.FitbitToken).get(session_id)

    def create(self, db: Session, obj: schemas.Token):
        db_obj = models.FitbitToken(
            session_id=obj.session_id,
            access_token=obj.access_token,
            expires_in=obj.expires_in,
            refresh_token=obj.refresh_token,
            scope=obj.scope,
            token_type=obj.token_type,
            user_id=obj.user_id,
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
