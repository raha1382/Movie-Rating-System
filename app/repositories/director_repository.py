from sqlalchemy.orm import Session
from app.models.director import Director

class DirectorRepository:

    def get_by_id(self, db: Session, director_id: int) -> Director | None:
        return db.query(Director).filter(Director.id == director_id).first()
