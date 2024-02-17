from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/<id>")
def get_cart_info(id):
    try:
        print(id)
        restaurant_data = mongo.db.CartDb.find_one({'_id': ObjectId(id)})
        
        if restaurant_data:
            serialized_data = dumps(restaurant_data)
            return ({"data":json.loads(serialized_data)}),200
        else:
            return jsonify({'error': 'User Cart not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@cart_bp.route("/", methods=["POST"])
def create_user_cart():
    try:
        postData = request.json

        mongo.db.CartDb.insert_one(
            {
                'Count':postData['count'], 
                'ProductId':ObjectId(postData['ProductId']),
                **postData,

            })
        return jsonify({ "message": "Cart Created Successfully" }), 200
    
    except Exception as e: 
        return jsonify({'error': str(e)}), 500  

@cart_bp.route("/", methods=["PUT"])
def update_cart_info():
    try:
        updateData = request.json
        cartId = updateData['_id']
        if not cartId:
            return jsonify({"message": "CartId is incorrect"}), 404
            
        updateData.pop('_id', None)
        result = mongo.db.CartDb.find_one_and_update({'_id':ObjectId(cartId)},{'$set': updateData})
        if result:
            return jsonify({'message': 'Cart Updated Successfully'}), 200
        else:
            return jsonify({'error': 'Cart not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
        
@cart_bp.route("/<id>", methods=["DELETE"])
def delete_user_cart(id):
    try:
        mongo.db.CartDb.delete_one({'_id':ObjectId(id)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

