from flask import Flask, render_template,request, redirect, url_for, session,g,send_file
from flask_pymongo import PyMongo
import bson
import re
import os
import PyPDF2

app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template("Jobify-AboutUs.html")

app.config['MONGO_URI'] = "mongodb://localhost:27017/Jobify_db"
app.secret_key = '123'
mongo = PyMongo(app)
users_collection = mongo.db.registration
collection =mongo.db.mycollection
users_collection_3=mongo.db.recruiter
app.config['UPLOAD_FOLDER'] = 'uploads'
#@app.route('/login')
#@app.route('/', methods=['GET', 'POST'])
# def login():
    
#     if request.method == "POST":
#        #data=request.form
#        username = request.form["username"]
#        password = request.form["password"]
#        print(username)
#        print(password)
#        user=users_collection.find_one({
#                 "username": username,
#                 "password": password
#             })
#        if user:
#            return render_template('UploadResume.html')
#        else:
#            return "User Not found"
#     return render_template('Jobify-Login.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["username"]
        password = request.form["password"]
        if email == "admin@admin.com" and password == "admin":
            session['username'] = email
            return redirect(url_for('admin'))  # Redirect to the admin page
        user = users_collection.find_one({
            "username": email,
            "password": password
        })

        if user:
            usertype = user.get("usertype")
            if usertype:
                session['username'] = email
                if usertype == "recruiter":
                    return redirect(url_for('rh'))  # Redirect to the recruiter page
                elif usertype == "candidate":
                    return redirect(url_for('ch'))  # Redirect to the candidate page
                else:
                    return "<script>alert('Invalid user type');</script>"
            else:
                return "<script>alert('Username not found in user data');</script>"
        else:
            return "<script>alert('User not found');</script>"

    return render_template('Jobify-Login.html')




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        return redirect(url_for('login')) 
    return render_template("Jobify-SignUp.html")

@app.route('/candidatesignup', methods=['GET', 'POST'])
def signupc():
    # if request.method == "POST":
    #     return redirect(url_for('login')) 
    # return render_template("Jobify-CandidateSignUp.html")
    if request.method == "POST":
        full_name = request.form["full_name"]
        username = request.form["username"]
        usertype = "candidate"
        contact_no = request.form["contact_no"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match"

        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            return "Username already exists"

        new_user = {
            "name": full_name,
            "username": username,
            "usertype": usertype,
            "contactNo": contact_no,
            "password": password
        }
        users_collection.insert_one(new_user)
        return "User registered successfully"
    
    return render_template("Jobify-CandidateSignUp.html")

# @app.route('/get_candidates', methods=['GET', 'POST'])
# def get_candidates():
#     candidates = list(users_collection.find({"usertype": "candidate"}, {"name": 1}))

#     data = {
#         "candidates": [candidate["name"] for candidate in candidates]
#     }

#     return jsonify(data)


# @app.route('/get_recruiters', methods=['GET', 'POST'])
# def get_recruiters():
#     recruiters = list(users_collection.find({"usertype": "recruiter"}, {"name": 1}))

#     data = {
#         "recruiters": [recruiter["name"] for recruiter in recruiters]
#     }

#     return jsonify(data)


@app.route('/recruitersignup', methods=['GET', 'POST'])
def signupr():
    # if request.method == "POST":
    #    return redirect(url_for('login')) 
    # return render_template("Jobify-RecruiterSignUp.html")
    if request.method == "POST":
        full_name = request.form["full_name"]
        username = request.form["username"]
        usertype = "recruiter"
        contact_no = request.form["contact_no"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            return "Username already exists"

        new_user = {
            "name": full_name,
            "username": username,
            "usertype": usertype,
            "contactNo": contact_no,
            "password": password
        }
        users_collection.insert_one(new_user)
        return "User registered successfully"
        
    
    return render_template("Jobify-RecruiterSignUpAshwin.html")

@app.route('/ch', methods=['GET', 'POST'])
def ch():
    return render_template("Jobify-CandidateHome.html")
@app.route('/rh', methods=['GET', 'POST'])
def rh():
    return render_template("Jobify-RecruiterHomeAsh.html")
@app.route('/rf', methods=['GET', 'POST'])
def rf():
    return render_template("Jobify-RecruiterFilter.html")
@app.route('/vd', methods=['GET', 'POST'])
def joel_data():
    ee=session['username']
    print(ee)
    joel_data = collection.find_one({'email':ee})

    return render_template("ViewDetailsJoel.html",joel_data=joel_data)

@app.route('/filter', methods=['GET', 'POST'])
def fil():
    cgpa_filter = request.args.get('cgpa_filter')
    duration_filter = request.args.get('duration_filter')

    cgpa_filter_conditions = {
        "6 to 7": {"$gte": 6.0, "$lt": 7.0},
        "7 to 8": {"$gte": 7.0, "$lt": 8.0},
        "8 to 9": {"$gte": 8.0, "$lt": 9.0},
        "9 to 10": {"$gte": 9.0, "$lt": 10.0},
        "All": {}
    }

    duration_filter_conditions = {
        "0 to 12": {"$gte": 0, "$lt": 13},
        "13 to 24": {"$gte": 13, "$lt": 25},
        "Above 24": {"$gte": 25}
    }

    if not cgpa_filter:
        cgpa_filter = "All"

    if not duration_filter:
        duration_filter = "All"

    if cgpa_filter in cgpa_filter_conditions:
        cgpa_condition = cgpa_filter_conditions[cgpa_filter]
    else:
        cgpa_condition = {}

    if duration_filter in duration_filter_conditions:
        duration_condition = duration_filter_conditions[duration_filter]
    else:
        duration_condition = {}

    if cgpa_filter == "All" and duration_filter == "All":
        resumes = collection.find()
    elif cgpa_filter == "All":
        resumes = collection.find({'duration': duration_condition})
    elif duration_filter == "All":
        resumes = collection.find({'cgpa': cgpa_condition})
    else:
        resumes = collection.find({'$and': [{'cgpa': cgpa_condition}, {'duration': duration_condition}]})


    resumes_list = list(resumes)
    for resume in resumes_list:
        resume['duration'] = int(resume['duration'])  # Convert duration to integer


    num_resumes = len(resumes_list)

    no_data_message = "No data found for the selected filters." if num_resumes == 0 else ""
    return render_template("Jobify-RecruiterFilter.html",resumes=resumes_list, no_data_message=no_data_message)
@app.route('/admin')
def admin():
    # Fetch candidates and recruiters from MongoDB
    candidates = list(users_collection.find({"usertype": "candidate"}))
    recruiters = list(users_collection.find({"usertype": "recruiter"}))
    return render_template('Jobify-Admin.html', candidates=candidates, recruiters=recruiters)

@app.route('/upresume', methods=['GET', 'POST'])
def upload_form():
    return render_template('Jobify-CandidateUpload.html')
@app.route('/reresume', methods=['GET', 'POST'])
def rupload_form():
    return render_template('RecruiterUploadAsh.html')
@app.route('/reup', methods=['GET', 'POST'])
def recupload_form():
    # Get the uploaded file
    file = request.files['file']

    # Save the file to the destination folder
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    # Convert the file to a BSON object
    bson_object = bson.BSON.encode({'file_data': file.read()})

    # Store the file name and BSON file in MongoDB
    document = {
        'filename': file.filename,
        'file_bson': bson_object
    }
    users_collection_3.insert_one(document)

    return render_template('Jobify-RecruiterHomeAsh.html', message='File Uploaded Successfully')

  
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('upload_form.html', error='No file part')

    file = request.files['file']
    if file.filename == '':
        return render_template('upload_form.html', error='No selected file')

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        pdf_text = extract_text_from_pdf(file_path)

         # Define the data to insert into MongoDB
        data = {}

        lines = pdf_text.split('\n')
        for line in lines:
            parts = line.split(':', 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                # Use regular expressions to check if the value is a number
                if re.match(r'^-?\d+(?:\.\d+)?$', value):
                    # If it's a number, convert it to an integer
                    data[key] = float(value)
                
                else:
                    # If it's not a number, keep it as a string
                    data[key] = value

        # Insert data into MongoDB
        collection.insert_one(data)

        return render_template('Jobify-CandidateUpload.html', pdf_text=pdf_text)




@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'file' not in request.files:
        return render_template('Jobify-CandidateUpload.html', error='No file part')

    file = request.files['file']
    if file.filename == '':
        return render_template('Jobify-CandidateUpload.html', error='No selected file')

    pdf_text = extract_text_from_pdf(file)
    
   


    return render_template('Jobify-CandidateUpload.html', pdf_text=pdf_text)

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    pdf_text = ''

    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    # Split the text into lines and format each line
    formatted_lines = []

    for line in pdf_text.split('\n'):
        # Split each line by the first occurrence of a space and a colon
        parts = line.split(' :', 1)
        
        if len(parts) == 2:
            # If there are two parts, it's a field name and value
            field_name, field_value = parts
            formatted_line = f"{field_name.strip()} : {format_value(field_value.strip())}"
        elif len(parts) == 1:
            # If there's only one part, it's a field value without a field name
            formatted_line = format_value(parts[0].strip())
        else:
            formatted_line = line.strip()
        
        formatted_line = formatted_line.lower()
        formatted_lines.append(formatted_line)

    # Join the lines back together with line breaks
    formatted_pdf_text = '\n'.join(formatted_lines)

    return formatted_pdf_text
def format_value(value):
    # Use a regular expression to check if the value is a number
    if re.match(r'^-?\d+(?:\.\d+)?$', value):
        # If it's a number, convert it to an integer
        return float(value)
    else:
        # If it's not a number, keep it as a string
        return value  
@app.route('/download_file', methods=['GET','POST'])
def download_file():
    p='D:/Flask/Cloud/uploads/FORMAT_RESUME.pdf'
    return send_file(p,as_attachment=True)
# @app.route('/joel_data')
# def joel_data():
    
#     # Retrieve data for the person named 'Joel'
#     joel_data = collection.find_one({'name': 'red'})
#     #print(joel_data.items())

#     return render_template('ViewDetails.html', joel_data=joel_data)
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 80)
