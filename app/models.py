from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主建
    username = db.Column(db.String(20), unique=True, nullable=False)  # 不可重复，非空
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
