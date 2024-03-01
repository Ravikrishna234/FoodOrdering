from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from db import mongo
from bson.json_util import dumps
import json
customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/<id>")
def get_user(id):
    try:
        print(id)
        userData = mongo.db.Customers.find_one({"_id":ObjectId(id)})
        print(userData)
        if userData:
            return jsonify({
                "status":"Success",
                "data":userData,
            }),200
        else:
            return jsonify({"status":"Error","message":"user details are not found"})
    except Exception as e:
        return e

@customers_bp.route("/", methods=["POST"])
def create_user():
    try:
        postData = request.json
        postData['role'] = "customer"
        result = mongo.db.Customers.insert_one(postData)
        if result:
            inserted_user = mongo.db.Customers.find_one({'_id':result.inserted_id})
            inserted_user['_id'] = str(inserted_user['_id'])
            return jsonify({
                "status":"Success",
                "message": "User Created Successfully",
                "data":json.loads(dumps(inserted_user))
            }), 200
    except Exception as e:
        return e

@customers_bp.route("/", methods=["PUT"])
def update_user():
    try:
        updateData = request.json
        userId = updateData['_id']
        del updateData['_id']
        result = mongo.db.Customers.find_one_and_update({'_id':ObjectId(userId)},{'$set': updateData})
        if result:
            return jsonify({
                "status":"Success",
                'message': 'User Updated Successfully',
                "data":json.loads(dumps(result))
            }), 200
        else:
            return jsonify({"status":"Success","message":"Error in Updating"})
    except Exception as e:
        print(e)
        return e
