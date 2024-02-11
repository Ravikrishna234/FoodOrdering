from .customer import customers_bp
from .product import products_bp

def init_app(app):
    app.register_blueprint(customers_bp, url_prefix="/customers")
    app.register_blueprint(products_bp, url_prefix="/products")

