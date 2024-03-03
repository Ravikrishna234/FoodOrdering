from .product import products_bp
from .restaurant import restaurants_bp
from .cart import cart_bp
from .orders import orders_bp
from .address import address_bp
from .register import register_bp
from .register import login_bp
from .transaction import transactions_bp

def init_app(app):
    app.register_blueprint(register_bp, url_prefix="/register")
    app.register_blueprint(login_bp,url_prefix="/login")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(restaurants_bp, url_prefix="/restaurants")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(address_bp, url_prefix="/customerAddresses")
    app.register_blueprint(transactions_bp, url_prefix="/transaction")

    

