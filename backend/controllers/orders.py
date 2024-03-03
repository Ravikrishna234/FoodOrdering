from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson import json_util
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
 
def get_order_total(records, index):
        order_total = 0
        records[index]['_id'] = str(records[index]['_id'])
        records[index]['customerId'] = str(records[index]['customerId'])
        records[index]['restaurantId'] = str(records[index]['restaurantId'])
        records[index]['transactionId'] = str(records[index]['transactionId'])
        records[index]['orderDate'] = records[index]['orderDate'].strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        #fetch address for single order
        orderAddress = get_order_address(records[index]['addressId'])

        desired_fields = {
            "city": orderAddress["city"],
            "country": orderAddress["country"],
            "postalCode": orderAddress["postalCode"],
            "state": orderAddress["state"],
            "streetAddress": orderAddress["streetAddress"]
        }
        records[index]['address'] = desired_fields

        records[index].pop('addressId',None)
        for j in range(len(records[index]["product"])):
            records[index]["product"][j]['_id'] = str(records[index]["product"][j]['_id'])
            order_total += records[index]["product"][j]["price"]
        return records,order_total

def get_order_address(addressId=None):
    print(addressId)
    if addressId:
        addressRecord = mongo.db.CustomerAddress.find_one({"_id":ObjectId(addressId)})
        return addressRecord


@orders_bp.route("/user",methods=["GET"])
def get_all_orders():
    try:
        customerId = request.args.get('customerId')
        admin = request.args.get('admin')
        allRecord = []
        if admin == "True":
            allRecord = list(mongo.db.Orders.find({}))      
        else:
            customerId = request.args.get('customerId')
            allRecord = list(mongo.db.Orders.find({'customerId': ObjectId(customerId)}))
                
        for i in range(len(allRecord)):
            allRecord, allRecord[i]['orderTotal'] = get_order_total(allRecord, i)  
        if(len(allRecord)):                                               
            return jsonify({"status":"Success",
                            "message":"User orders fetched successfully",
                            "data":json.loads(dumps(allRecord))})
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
        result_field = {}
        result = mongo.db.Orders.find_one_and_update({'_id':ObjectId(orderId)},{'$set': {'orderStatus': updateData['orderStatus']}})
        if result:
            result_field['_id'] = str(result['_id'])
            result_field['orderStatus'] = result['orderStatus']

            return jsonify({"status":"Success",'message': 'Order Updated Successfully',"data":json.loads(dumps(result_field))}), 200
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

