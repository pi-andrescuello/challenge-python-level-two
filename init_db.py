from app.db.base import engine
from app.db.models.user_model import Base as UserModel

UserModel.metadata.create_all(bind=engine)