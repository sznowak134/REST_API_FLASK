from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_restful import Api

from db import db
from resources.user import (UserRegister,
                            User,
                            UserLogin,
                            UserLogout,
                            TokenRefresh)
from resources.category import Category, CategoryList
from blacklist import BLACKLIST
from resources.item import Item, ItemList
from resources.cart import Cart, UserCart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.config['JWT_SECRET_KEY'] = True
app.secret_key = 'Szymon'  #
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return{'is_admin': True}
    return{'is_admin': False}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader     # jwt is a variable from line 23
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader  # when the token which was sent to us is not an actual jwt
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader  # when jwt was not sent at all
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader  # non fresh token but we required fresh token
def token_not_fresh_callback():
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    })


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(CategoryList, '/categories')
api.add_resource(Category, '/category/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Cart, '/cart/<int:item_id>')
api.add_resource(UserCart, '/user/cart')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
