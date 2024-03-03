from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json
from marshmallow import Schema, fields

restaurants_bp = Blueprint("restaurants", __name__)

class RestaurantSchema(Schema):
    name=fields.Str(required=True)
    location=fields.Str(required=True)

class RestaurantUpdateSchema(Schema):
    _id=fields.Str(required=True)
    name=fields.Str()
    location=fields.Str()

restaurant_schema = RestaurantSchema()
restaurant_update_schema = RestaurantUpdateSchema()


@restaurants_bp.route("/", methods=["GET"])
def get_all_restaurants():
    try:
        restaurantProductCollection = []
        get_all_restaurants_data = mongo.db.Restaurants.find()
        for restaurant_data in get_all_restaurants_data:
            restaurant_id = str(restaurant_data['_id'])
            mono_restaurant_data = get_restaurant(restaurant_id, flag='GETALL')
            print("Mono Restaurant Collection", mono_restaurant_data)
            if mono_restaurant_data:
                restaurantProductCollection.append(mono_restaurant_data)
            else:
                print(f"No details found for restaurant ID: {restaurant_id}")

        return jsonify({"status":"Success","data": restaurantProductCollection}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@restaurants_bp.route("/<id>")
def get_restaurant(id, flag=None):
    try:
        print(id)
        restaurant_id = ObjectId(id)

        pipeline = [
            {
                '$match': {
                    '_id': restaurant_id  # Match the specified restaurant
                }
            },
            {
                '$lookup': {
                    'from': 'Products',  # Name of the Products collection
                    'localField': '_id',  # Field from the Restaurants collection
                    'foreignField': 'restaurantId',  # Field from the Products collection
                    'as': 'products'  # Name of the field to store the matched products
                }
            }
        ]
        restaurant_with_products = list(mongo.db.Restaurants.aggregate(pipeline))
        print(restaurant_with_products)

        if restaurant_with_products:
            for product in restaurant_with_products[0]['products']:
                product['_id'] = str(product['_id'])
                product['restaurantId'] = str(product['restaurantId'])
        
            restaurant_with_products[0]['_id'] = str(restaurant_with_products[0]['_id'])            
            
            # print(restaurant_with_products)
            # serialized_data = dumps(product_data)
            if(flag == "GETALL"):
                return restaurant_with_products[0]
            
            return jsonify({"status":"Success","data": restaurant_with_products[0]}), 200
        else:
            return jsonify({"status":"Error",'message': 'Restaurant not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  


@restaurants_bp.route("/", methods=["POST"])
def create_restaurant():
    try:
        postData = request.json
        errors = restaurant_schema.validate(postData)
        if errors:
            return jsonify({'error': errors}), 400
        result = mongo.db.Restaurants.insert_one(postData)
        if result:
            inserted_restaurant = mongo.db.Restaurants.find_one({'_id':ObjectId(result.inserted_id)})
            inserted_restaurant['_id'] = str(inserted_restaurant['_id'])
            return jsonify({ "status":"Success","message": "Restaurant Created Successfully" ,"data":inserted_restaurant}), 200
        else:
            return jsonify({"status":"Error","message":"Restaurant was not created"}), 500
    
    except Exception as e: 
        return jsonify({'error': str(e)}), 500  

@restaurants_bp.route("/", methods=["PATCH"])
def update_restaurant():
    try:
        updateData = request.json
        errors = restaurant_update_schema.validate(updateData)
        if errors:
            return jsonify({'error': errors}), 400
        restaurantId = updateData['_id']
        updateData.pop('_id', None)
        result = mongo.db.Restaurants.find_one_and_update({'_id':ObjectId(restaurantId)},{'$set': updateData})
        if result:
            result['_id'] = str(result['_id'])
            return jsonify({"status":"Success",'message': 'Restaurant Details Updated Successfully',"data":json.loads(dumps(result))}), 200
        else:
            return jsonify({"status":"Error",'message':'Restaurant not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

