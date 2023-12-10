from app.models.user import User

class UserRepo:
    def by_id(self, user_id: int) -> User:
        return User.query.filter_by(id=user_id).first()
    
    def by_username(self, username: str) -> User:
        return User.query.filter_by(username=username).first()