from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/new"
mongo = PyMongo(app)
users_collection = mongo.db.registration

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')

        user = users_collection.find_one({'email': username, 'password': password})
        if user:
            return "Logged in successfully!"
        else:
            return "Login failed. Invalid credentials."

    return render_template('Jobify-Login.html')

if __name__ == '__main__':
    app.run(debug=True)
