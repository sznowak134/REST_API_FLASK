from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.category import CategoryModel


class Category(Resource):
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {'message': 'Category not found'}, 404

    @jwt_required
    def post(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': "Admin privilege required."}, 401

        if CategoryModel.find_by_name(name):
            return {'message': "A category with name '{}' already exists".format(name)}, 404

        category = CategoryModel(name)

        try:
            category.save_to_db()
        except:
            return{'message': "An error occurred creating the category"}, 500  # internal server error

        return category.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': "Admin privilege required."}, 401

        category = CategoryModel.find_by_name(name)
        if category:
            category.delete_from_db()
        return {'message': 'Category deleted'}, 204


class CategoryList(Resource):
    def get(self):
        return {'Category': [category.json() for category in CategoryModel.find_all()]}
