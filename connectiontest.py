from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure the MongoDB URI (connection string) and database name
app.config['MONGO_URI'] = 'mongodb://localhost:27017/new'

# Initialize the PyMongo extension
mongo = PyMongo(app)
@app.route('/')
def index():
    # Access a collection
    collection = mongo.db.registration
    if collection.find_one({"username": "skm@gmail.com"}):
        return "Username already exists!"
    else :
        return "Username"

if __name__ == '__main__':
    app.run()
