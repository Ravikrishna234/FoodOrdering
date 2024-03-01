from flask import Flask, jsonify
from db import mongo
from flask_cors import CORS


from controllers import init_app as controller_init

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = "mongodb+srv://ravikrishnakbf257:Ironman123@cluster0.ipsx71s.mongodb.net/foodordering?retryWrites=true&w=majority"

mongo.init_app(app)

controller_init(app)

@app.route("/")
def test():
    try:
        user = mongo.db.users.find_one({"email":"admin@gmail.com"})
        if not user:
            mongo.db.users.insert_one({
                'firstName': "admin",
                "email":"admin@gmail.com",
                "password":"admin123",
                "role":"admin"
            })
            return jsonify({"message":"Admin created"})
        return "<h1>Working</h1>"
    except Exception as e:
        return jsonify({'message': "Error occured"})



app.run(debug=True)






