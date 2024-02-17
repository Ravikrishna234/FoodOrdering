from .customer import customers_bp
from .product import products_bp
from .restaurant import restaurants_bp
from .cart import cart_bp
from .orders import orders_bp
from .address import address_bp

def init_app(app):
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(restaurants_bp, url_prefix="/restaurants")
    app.register_blueprint(cart_bp, url_prefix="/cart")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(address_bp, url_prefix="/customerAddresses")
    

