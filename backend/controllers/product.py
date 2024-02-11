from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from db import mongo
products_bp = Blueprint("products", __name__)


@products_bp.route("/<id>")
def get_product(id):
    try:
        productData = mongo.db.Products.find_one({"_id":id})
        return ({"data":productData}),200
    
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
        mongo.db.Products.find_one_and_update({'_id':ObjectId(productId)},{'$set': updateData})
        return jsonify({'message': 'Product Updated Successfully'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500  
      
@products_bp.route("/", methods=["DELETE"])
def delete_product():
    try:
        deleteData = request.json
        productId = deleteData['_id']
        deleteData.pop('_id', None)
        mongo.db.Products.deleteOne({'_id':ObjectId(productId)})
    except:
        return jsonify({'error': str(e)}), 500  

