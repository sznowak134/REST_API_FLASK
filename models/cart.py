from db import db


class CartModel(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    item = db.relationship('ItemModel')

    def __init__(self, item_id, user_id):
        self.item_id = item_id
        self.user_id = user_id

    def json(self):
        return{
            'item_id': self.item_id,
            'user_id': self.user_id
        }

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_item_id(cls, item_id):
        return cls.query.filter_by(item_id=item_id).all()

    @classmethod
    def find_by_item_user_id(cls,item_id, user_id):
        return cls.query.filter_by(item_id=item_id, user_id=user_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
