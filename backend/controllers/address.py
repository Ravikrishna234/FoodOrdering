from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json

address_bp = Blueprint("customeraddresses", __name__)


@address_bp.route("/<id>")
def get_customerAddress(id):
    try:
        print(id)
        addressDb = mongo.db.CustomerAddress.find_one({'_id': ObjectId(id)})
        
        if addressDb:
            serialized_data = dumps(addressDb)
            return ({"status":"Success","data":json.loads(serialized_data)}),200
        else:
            return jsonify({'error': 'Customer Address not found'}), 404
        
    except Exception as e:
        return jsonify({"status":"Error", 'error': str(e)}), 500  

@address_bp.route("/", methods=["POST"])
def create_customerAddress():
    try:
        postData = request.json
        
        address = mongo.db.CustomerAddress.insert_one(
            {
                **postData,
                'customerId':ObjectId(postData['customerId']), 
            })
        if address:
            inserted_address = mongo.db.CustomerAddress.find_one({"_id":address.inserted_id})
            inserted_address['_id'] = str(inserted_address['_id'])
            inserted_address['customerId'] = str(inserted_address['customerId'])
            return jsonify({"status":"Success", "message": "Customer Address Created Successfully","data":json.loads(dumps(inserted_address)) }), 200
    
    except Exception as e: 
        return jsonify({"status":"Error", 'error': str(e)}), 500  

@address_bp.route("/", methods=["PUT"])
def update_customerAddress():
    try:
        updateData = request.json
        addressId = updateData['_id']
        if not addressId:
            return jsonify({"status":"Error","message":"AddressId is incorrect"}), 400
        
        updateData.pop('_id', None)
        result = mongo.db.CustomerAddress.find_one_and_update({'_id':ObjectId(addressId)},{'$set': {'OrderStatus':updateData['OrderStatus']}})
        if result:
            result['_id'] = str(result['_id'])
            result['customerId'] = str(result['customerId'])
            return jsonify({"status":"Error", 'message': 'Customer Address Updated Successfully',"data":json.loads(dumps(result))}), 200
        else:
            return jsonify({"status":"Error", "message":'Customer Address not found' }), 404

    except Exception as e:
        print(e)
        return jsonify({"status":"Error", 'error': str(e)}), 500  
        
@address_bp.route("/<id>", methods=["DELETE"])
def delete_customerAddress(id):
    try:
        result = mongo.db.CustomerAddress.delete_one({'_id':id})
        if result:
            return jsonify({"status":"Success", "message":'Customer Address Deleted Sucessfully'}),200
        else:
            return jsonify({"status":"Error","message":'Customer Address not found' }), 404

    except Exception as e:
        return jsonify({"status":"Error", 'error': str(e)}), 500  

