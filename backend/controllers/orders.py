from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/<id>",methods=["GET"])
def get_order_info(id):
    try:
        print(id)
        order_data = mongo.db.Orders.find_one({'_id': ObjectId(id)})
        
        if order_data:
            serialized_data = dumps(order_data)
            return ({"status":"Success","data":json.loads(serialized_data)}),200
        else:
            return jsonify({"status":"Error",'error': 'User Cart not found'}), 404
        
    except Exception as e:
        return jsonify({"status":"Error",'error': str(e)}), 500 
 
@orders_bp.route("/user",methods=["GET"])
def get_all_orders(customerId=None):
    try:
        customerId = request.args.get('customerId')
        admin = request.args.get('admin', default=False, type=bool)
        if admin:
            allRecord = list(mongo.db.Orders.find({}))
            return jsonify({"data":json.loads(dumps(allRecord))})
        else:
            customerId = request.args.get('customerId')
            customerOrder = list(mongo.db.Orders.find({'customerId': ObjectId(customerId)}))

            for i in range(len(customerOrder)):
                order_total = 0
                print(i)
                for j in range(len(customerOrder[i]["product"])):
                    order_total += customerOrder[i]["product"][j]["price"]
                customerOrder[i]['orderTotal'] = order_total

            if(len(customerOrder)):
                return jsonify({"status":"Success",
                                "message":"User orders fetched successfully",
                                "data":json.loads(dumps(customerOrder))})
            return jsonify({"status":"Error","message":"No orders found for user"})
    except Exception as e:
        return jsonify({"status":"Error",'error': str(e)}), 500



@orders_bp.route("/", methods=["POST"])
def create_order_info():
    try:
        postData = request.json
        
        result = mongo.db.Orders.insert_one(
            {
                'OrderStatus': postData['OrderStatus'],
                **postData,

            })
        if result:
            return jsonify({"status":"Success","message": "Order Created Successfully","data":json.loads(dumps(result))}), 200 
    except Exception as e: 
        return jsonify({"status":"Error",'error': str(e)}), 500  

@orders_bp.route("/", methods=["PATCH"])
def update_order_info():
    try:
        updateData = request.json
        orderId = updateData['_id']
        updateData.pop('_id', None)
        result = mongo.db.Orders.find_one_and_update({'_id':ObjectId(orderId)},{'$set': {'OrderStatus': updateData['OrderStatus']}})
        if result:
            return jsonify({"status":"Success",'message': 'Order Updated Successfully'}), 200
        else:
            return jsonify({"status":"Error","message": "Order not found"}), 404

    except Exception as e:
        print(e)
        return jsonify({"status":"Error",'error': str(e)}), 500
        
@orders_bp.route("/<id>", methods=["DELETE"])
def delete_order(id):
    try:
        result = mongo.db.Orders.delete_one({'_id':ObjectId(id)})
        if result:
            return jsonify({"status":"Success","message": "Order Deleted Successfully"}), 200
        else:
            return jsonify({"status":"Success","message": "Order not found"}), 404
    except Exception as e:
        return jsonify({"status":"Error",'error': str(e)}), 500  

