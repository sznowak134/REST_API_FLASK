from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))  # kluczem jest id sklepu
    category = db.relationship('CategoryModel')

    cart = db.relationship('CartModel', lazy='dynamic')

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id

    def json(self):
        return{
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category_id': self.category_id
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, item_id):
        return cls.query.filter_by(id=item_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
