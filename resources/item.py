from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required,
                                fresh_jwt_required,
                                jwt_optional,
                                get_jwt_identity,
                                get_jwt_claims)

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank'
                        )
    parser.add_argument('category_id',
                        type=int,
                        required=True,
                        help='Every item needs a category id')

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': "Admin privilege required."}, 401

        if ItemModel.find_by_name(name):
            return {'message': 'An item with name {} already exists'.format(name)}, 404

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        return item.json(), 201

    @fresh_jwt_required
    def put(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': "Admin privilege required."}, 401

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': "Admin privilege required."}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return{'message': 'Item deleted'}
        return {'message': 'Item not found.'}, 404


class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return{'items': items}, 200

        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200
