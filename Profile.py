from flask import Flask, render_template
import pymongo

app = Flask(__name__)

# MongoDB connection setup
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["new"]
collection = db["mycollection"]

@app.route('/joel_data')
def joel_data():
    # Retrieve data for the person named 'Joel'
    joel_data = collection.find_one({'email':"ab@gmial.com"})

    return render_template('ViewDetails.html', joel_data=joel_data)

if __name__ == '__main__':
    app.run(debug=True)



