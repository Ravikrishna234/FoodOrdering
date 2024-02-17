from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json
products_bp = Blueprint("products", __name__)


@products_bp.route("/<id>")
def get_product(id):
    try:
        product_data = mongo.db.Products.find_one({'_id': ObjectId(id)})
        if product_data:
            serialized_data = dumps(product_data)
            return ({"data":json.loads(serialized_data)}),200
        else:
            return jsonify({'error': 'Product not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500   

@products_bp.route("/", methods=["POST"])
def create_product():
    try:
        postData = request.json
        mongo.db.Products.insert_one(postData)
        return jsonify({ "message": "Product Created Successfully" }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@products_bp.route("/", methods=["PUT"])
def update_product():
    try:
        updateData = request.json
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

