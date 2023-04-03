from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    api_key = db.Column(db.String(200), unique=True, nullable=False)
    subscription_level = db.Column(db.String(50), nullable=False, default='free')

    def __repr__(self):
        return f"User('{self.username}', '{self.subscription_level}')"
