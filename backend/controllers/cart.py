from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json
from marshmallow import Schema, fields

cart_bp = Blueprint("cart", __name__)
class CartSchema(Schema):
    count=fields.Float(required=True)
    customerId=fields.Str(required=True)
    productId=fields.Str(required=True)
    restaurantId=fields.Str(required=True)

cart_schema = CartSchema()

@cart_bp.route("/<id>")
def get_cart_info(id):
    try:
        print(id)
        cart_data = mongo.db.CartDb.find_one({'_id': ObjectId(id)})
        
        if cart_data:
            cart_data['_id']=str(cart_data['_id'])
            cart_data['customerId'] = str(cart_data['customerId'])
            cart_data['productId'] = str(cart_data['productId'])
            cart_data['restaurantId'] = str(cart_data['restaurantId'])
            serialized_data = dumps(cart_data)
            return ({"status":"Success","data":json.loads(serialized_data)}),200
        else:
            return jsonify({"status":"Error",'error': 'User Cart not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@cart_bp.route("/customer/<customerId>", methods=["GET"])
def get_cart_info_by_customer(customerId):
    try:
        product_cart = []
        customer = list(mongo.db.CartDb.find({'customerId': ObjectId(customerId)}))
        if customer:
            for key in customer:
                print("key",key)
                product = {}
                productData = list(mongo.db.Products.find({'_id': key["productId"]}))
                print(productData)
                restaurantData = list(mongo.db.Restaurants.find({'_id':productData[0]["restaurantId"]}))
                restaurantData[0]["_id"] = str(restaurantData[0]["_id"])
                product["_id"] = str(key["_id"])
                product["productId"] = str(productData[0]["_id"])
                product["restaurantId"] = restaurantData[0]["_id"]
                product["count"] = key["count"]
                product["name"] = productData[0]["name"]
                product["price"] = productData[0]["price"]
                print(product)
                product_cart.append(product)
                print(product_cart)
           

        if len(product_cart):    
            return jsonify({"status":"Success", "data": {
                "product":product_cart,
            }}), 200
        else:
            return jsonify({"status":"Error","data": "No Items in Cart"}), 200
    except Exception as e:
       return jsonify({"status":"Error",'error': str(e)}), 500

@cart_bp.route("/", methods=["POST"])
def create_user_cart():
    try:
        postData = request.json
        errors = cart_schema.validate(postData)
        if errors:
            return jsonify({"error":errors,"message":"Missing Required Fields"})
        postData['customerId'] = ObjectId(postData['customerId'])
        postData['productId'] = ObjectId(postData['productId'])
        postData['restaurantId'] = ObjectId(postData['restaurantId'])
        result = mongo.db.CartDb.insert_one(postData)
        if result:
            inserted_cartData = mongo.db.CartDb.find_one({'_id':result.inserted_id})
            inserted_cartData['_id'] = str(inserted_cartData['_id'])
            inserted_cartData['customerId'] = str(inserted_cartData['customerId'])
            inserted_cartData['productId'] = str(inserted_cartData['productId'])
            inserted_cartData['restaurantId'] = str(inserted_cartData['restaurantId'])
            return jsonify({ "status":"Success","message": "Cart Created Successfully","data":json.loads(dumps(inserted_cartData)) }), 200
    
    except Exception as e: 
        return jsonify({"status":"Error",'error': str(e)}), 500  

@cart_bp.route("/", methods=["PATCH"])
def update_cart_info():
    try:
        updateData = request.json
        cartId = updateData['_id']
        productId = updateData['productId']
        if not cartId:
            return jsonify({"status":"Error","message": "CartId is incorrect"}), 404
        if not productId:
            return jsonify({"status":"Error","message":"productId is incorrect"}), 404
        updateData.pop('_id', None)
        updateData.pop('productId', None)
        result = mongo.db.CartDb.find_one_and_update({'_id':ObjectId(cartId),'productId':ObjectId(productId)},{'$set': updateData})
        if result:
            result['_id'] = str(result['_id'])
            result['customerId'] = str(result['customerId'])
            result['productId'] = str(result['productId'])
            result['restaurantId'] = str(result['restaurantId'])
            
            return jsonify({"status":"Success",'message': 'Cart Updated Successfully',"data":json.loads(dumps(result))}), 200
        else:
            return jsonify({"status":"Error",'error': 'Cart not found'}), 404

    except Exception as e:
        print(e)
        return jsonify({"status":"Error",'error': str(e)}), 500
        
@cart_bp.route("/<id>", methods=["DELETE"])
def delete_user_cart(id):
    try:
        result = mongo.db.CartDb.delete_one({'_id':ObjectId(id)})
        if result:
            return jsonify({"status":"Success", "message":"User Cart Deleted"})
        else:
            return jsonify({"status":"Error","message":"Error in Deleting User Cart"})
    except Exception as e:
        return jsonify({"status":"Error",'error': str(e)}), 500  

