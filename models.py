from flask_login import UserMixin
from datetime import datetime, timezone
from ext import app, db, login_manager
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    img = db.Column(db.String)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)




class User(db.Model, BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    articles = db.relationship('Article', backref='author', lazy=True)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
