from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from bson.json_util import dumps
from db import mongo
import json
from marshmallow import Schema, fields
transactions_bp = Blueprint("transactions", __name__)

class TransactionSchema(Schema):
    Amount = fields.Str(required=True)
    restaurantId=fields.Str(required=True)
    paymentId=fields.Str(required=True)
    orderId=fields.Str(required=True)


transaction_schema = TransactionSchema()

@transactions_bp.route("/<id>")
def get_transaction(id):
    try:
        print({'_id': ObjectId(id)})
        transaction_data = mongo.db.Transactions.find_one({'_id': ObjectId(id)})
        if transaction_data:
            transaction_data['_id'] = str(transaction_data['_id'])
            transaction_data['restaurantId'] = str(transaction_data['restaurantId'])
            transaction_data['paymentId'] = str(transaction_data['paymentId'])
            transaction_data['orderId'] = str(transaction_data['orderId'])

            return ({"data":transaction_data}),200
        else:
            return jsonify({'error': 'Transaction not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500   


@transactions_bp.route("/", methods=["POST"])
def create_transaction():
    try:
        postData = request.json
        errors = transaction_schema.validate(postData)
        if errors:
            return jsonify({'error': errors}), 400
        restaurant_id = ObjectId(postData['restaurantId'])
        payment_id = ObjectId(postData['paymentId'])
        order_id = ObjectId(postData['orderId'])

        postData.pop('restaurantId')
        postData.pop('payment_id')
        postData.pop('order_id')

        mongo.db.Products.insert_one(
            {'restaurantId':restaurant_id, 'paymentId':payment_id, 'orderId': order_id,**postData}
        )
        return jsonify({ "message": "Product Created Successfully" }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500  