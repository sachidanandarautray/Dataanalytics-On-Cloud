from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)

# Set up a MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["resume_extraction"]
collection = db["mycollection"]

@app.route('/')
def index():
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

    return render_template('re.html', resumes=resumes_list, no_data_message=no_data_message)

if __name__ == '__main__':
    app.run(debug=True)
