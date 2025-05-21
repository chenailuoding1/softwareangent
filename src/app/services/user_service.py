from sqlalchemy.orm import Session
from app.models.user import User
from .password_util import verify_password


class UserService:
    @staticmethod
    def create_user(db: Session, username: str, email: str, password: str):
        if UserService.get_user_by_username(db, username):
            raise ValueError("Username already exists")

        hashed_pwd = "hashed_" + password  # 模拟密码哈希
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed_pwd
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = UserService.get_user_by_username(db, username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()