from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)   # setting id to be a primary key
    username = db.Column(db.String(80))  # max 80 chars
    password = db.Column(db.String(80))

    cart = db.relationship('CartModel', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()   # query = SELECT * FROM users

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
