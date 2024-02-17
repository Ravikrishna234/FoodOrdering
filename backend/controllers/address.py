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
            return ({"data":json.loads(serialized_data)}),200
        else:
            return jsonify({'error': 'Customer Address not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@address_bp.route("/", methods=["POST"])
def create_customerAddress():
    try:
        postData = request.json
        
        mongo.db.CustomerAddress.insert_one(
            {
                **postData,
                'CustomerId':ObjectId(postData['CustomerId']), 
            })
        return jsonify({ "message": "Customer Address Created Successfully" }), 200
    
    except Exception as e: 
        return jsonify({'error': str(e)}), 500  

@address_bp.route("/", methods=["PUT"])
def update_customerAddress():
    try:
        updateData = request.json
        addressId = updateData['_id']
        if not addressId:
            return jsonify({"message":"AddressId is incorrect"}), 400
        
        updateData.pop('_id', None)
        result = mongo.db.CustomerAddress.find_one_and_update({'_id':ObjectId(addressId)},{'$set': {'OrderStatus':updateData['OrderStatus']}})
        if result:
            return jsonify({'message': 'Customer Address Updated Successfully'}), 200
        else:
            return jsonify({"message":'Customer Address not found' }), 404

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
        
@address_bp.route("/<id>", methods=["DELETE"])
def delete_customerAddress(id):
    try:
        result = mongo.db.CustomerAddress.deleteOne({'_id':id})
        if result:
            return jsonify({"message":'Customer Address Deleted Sucessfully'}),200
        else:
            return jsonify({"message":'Customer Address not found' }), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500  

