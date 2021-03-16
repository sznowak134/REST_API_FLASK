from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.cart import CartModel
from models.item import ItemModel


class Cart(Resource):
    @jwt_required
    def post(self, item_id):
        if CartModel.find_by_item_id(item_id):
            return {'message': 'An item with id {} already exists in your cart'.format(item_id)}, 404
        if not ItemModel.find_by_id(item_id):
            return {'message': 'There is no such an item in our stock'}, 404

        user_id = get_jwt_identity()
        item = CartModel(item_id, user_id)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        return item.json(), 201   # request has succeeded (new resource has been created)

    @jwt_required
    def delete(self, item_id):
        user_id = get_jwt_identity()
        item = CartModel.find_by_item_user_id(item_id, user_id)

        if not item:
            return {'message': 'Item not found'}, 404
        item.delete_from_db()
        return {'message': 'Item deleted'}, 202  # deleted successfully


class UserCart(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in CartModel.find_by_user_id(user_id)]
        if items:
            return {'cart_items': items}, 200
        return {'message': 'There is no items in your cart'}, 404
