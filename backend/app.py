from flask import Flask
from db import mongo
from controllers import init_app as controller_init
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://ravikrishnakbf257:Ironman123@cluster0.ipsx71s.mongodb.net/foodordering?retryWrites=true&w=majority"

mongo.init_app(app)

controller_init(app)

@app.route("/")
def test():
    return "<h1>Working</h1>"

app.run()






