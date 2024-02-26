from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json
from marshmallow import Schema, fields
products_bp = Blueprint("products", __name__)

class ProductSchema(Schema):
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    veg=fields.Bool(required=True)
    category=fields.Str(required=True)
    restaurantId=fields.Str(required=True)

class ProductUpdateSchema(Schema):
    _id = fields.Str(required=True)
    name = fields.Str()
    price = fields.Float()
    veg = fields.Bool()
    category = fields.Str()
    restaurantId = fields.Str(required=True)

product_schema = ProductSchema()
product_update_schema = ProductUpdateSchema()


@products_bp.route("/<id>")
def get_product(id):
    try:
        print({'_id': ObjectId(id)})
        product_data = mongo.db.Products.find_one({'_id': ObjectId(id)})
        if product_data:
            product_data['_id'] = str(product_data['_id'])
            product_data['restaurantId'] = str(product_data['restaurantId'])

            return ({"data":product_data}),200
        else:
            return jsonify({'error': 'Product not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500   


@products_bp.route("/", methods=["POST"])
def create_product():
    try:
        postData = request.json
        errors = product_schema.validate(postData)
        if errors:
            return jsonify({'error': errors}), 400
        restaurant_id = ObjectId(postData['restaurantId'])
        postData.pop('restaurantId')
        mongo.db.Products.insert_one(
            {'restaurantId':restaurant_id,  **postData}
        )
        return jsonify({ "message": "Product Created Successfully" }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@products_bp.route("/", methods=["PUT"])
def update_product():
    try:
        updateData = request.json
        errors = product_update_schema.validate(updateData)
        if errors:
            return jsonify({'error': errors}), 400
        
        restaurant_id = ObjectId(updateData['restaurantId'])
        updateData.pop('restaurantId')
        productId = updateData['_id']
        updateData.pop('_id', None)
        result = mongo.db.Products.find_one_and_update({'_id':ObjectId(productId)},{'$set': updateData})
        if result:
            return jsonify({'message': 'Product Updated Successfully'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500  
      
@products_bp.route("/<id>", methods=["DELETE"])
def delete_product(id):
    try:
        result = mongo.db.Products.delete_one({'_id':ObjectId(id)})
        if result:
            return jsonify({'message': 'Product Deleted Successfully'}), 200
        else:
            return jsonify({'message': 'Product not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

