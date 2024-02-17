from flask import Blueprint, request
from bson.objectid import ObjectId
from db import mongo
customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/<id>")
def get_user(id):
    try:
        print(id)
        userData = mongo.db.Customers.find_one({"_id":ObjectId(id)})
        print(userData)
        return {
            "data":userData,
        },200
    except Exception as e:
        return e

# @customers_bp.route("/", methods=["POST"])
# def create_user():
#     try:
#         postData = request.json
#         mongo.db.Customers.insert_one(postData)
#         return {
#             "message": "User Created Successfully"
#         }, 200
#     except Exception as e:
#         return e

@customers_bp.route("/", methods=["PUT"])
def update_user():
    try:
        updateData = request.json
        userId = updateData['_id']
        del updateData['_id']
        mongo.db.Customers.find_one_and_update({'_id':ObjectId(userId)},{'$set': updateData})
        return {
            'message': 'User Updated Successfully'
        }, 200
    except Exception as e:
        print(e)
        return e
