from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(80), nullable = True)

    @staticmethod
    def create_user(email, password, first_name, last_name,user_id):
        hashed_password = generate_password_hash(password)
        new_user = Users(email=email, password=hashed_password, first_name=first_name, last_name=last_name, user_id = user_id)
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def __repr__(self):
        return f'<User {self.email}>'

    @staticmethod
    def check_password(user, password):
        """Check hashed password against provided password."""
        return check_password_hash(user.password, password)
