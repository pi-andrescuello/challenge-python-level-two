from fastapi.params import Depends
from app.db.base import get_db

from sqlalchemy.orm import Session
from app.core.bcrypt import hash_password

from app.db.models.user_model import UserModel
from app.db.base import get_db

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self):
        return self.db.query(UserModel).all()

    def save(self, user: UserModel):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(UserModel).filter_by(email=email).first()
    
    def update_user(self, userModel, user_id):
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user:
            user.photo = userModel.photo
            user.user_name = userModel.user_name
            user.full_name = userModel.full_name
            user.password = hash_password(userModel.password)
            user.role = userModel.role

            self.db.commit()
            self.db.refresh(user)
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="udpate user, in get datos for update"
            )
    
    def delete_user(self, user_id):
        # Identify for user_id
        user = self.db.query(UserModel).filter_by(id=user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return self.db.query(UserModel).all()