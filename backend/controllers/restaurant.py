from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json

restaurants_bp = Blueprint("restaurants", __name__)


@restaurants_bp.route("/<id>")
def get_restaurant(id):
    try:
        restaurant_data = mongo.db.Restaurants.find_one({'_id': ObjectId(id)})
        if restaurant_data:
            serialized_data = dumps(restaurant_data)
            return ({"data":json.loads(serialized_data)}),200
        else:
            return jsonify({'error': 'Restaurant not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@restaurants_bp.route("/", methods=["POST"])
def create_restaurant():
    try:
        postData = request.json
        result = mongo.db.Restaurants.insert_one(postData)
        if result:
            return jsonify({ "message": "Restaurant Created Successfully" }), 200
        else:
            return jsonify({"message":"Restaurant was not created"}), 500
    
    except Exception as e: 
        return jsonify({'error': str(e)}), 500  

@restaurants_bp.route("/", methods=["PUT"])
def update_restaurant():
    try:
        updateData = request.json
        restaurantId = updateData['_id']
        updateData.pop('_id', None)
        result = mongo.db.Restaurants.find_one_and_update({'_id':ObjectId(restaurantId)},{'$set': updateData})
        if result:
            return jsonify({'message': 'Restaurant Details Updated Successfully'}), 200
        else:
            return jsonify({'message':'Restaurant not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

