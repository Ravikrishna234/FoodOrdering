from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/<id>")
def get_order_info(id):
    try:
        print(id)
        order_data = mongo.db.Orders.find_one({'_id': ObjectId(id)})
        
        if order_data:
            serialized_data = dumps(order_data)
            return ({"data":json.loads(serialized_data)}),200
        else:
            return jsonify({'error': 'User Cart not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@orders_bp.route("/", methods=["POST"])
def create_order_info():
    try:
        postData = request.json
        
        mongo.db.Orders.insert_one(
            {
                'OrderStatus': postData['OrderStatus'],
                **postData,

            })
        return jsonify({ "message": "Order Created Successfully" }), 200
    
    except Exception as e: 
        return jsonify({'error': str(e)}), 500  

@orders_bp.route("/", methods=["PUT"])
def update_order_info():
    try:
        updateData = request.json
        orderId = updateData['_id']
        updateData.pop('_id', None)
        result = mongo.db.Orders.find_one_and_update({'_id':ObjectId(orderId)},{'$set': {'OrderStatus': updateData['OrderStatus']}})
        if result:
            return jsonify({'message': 'Order Updated Successfully'}), 200
        else:
            return jsonify({"message": "Order not found"}), 404

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
        
@orders_bp.route("/<id>", methods=["DELETE"])
def delete_order(id):
    try:
        result = mongo.db.Orders.delete_one({'_id':ObjectId(id)})
        if result:
            return jsonify({"message": "Order Deleted Successfully"}), 200
        else:
            return jsonify({"message": "Order not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

