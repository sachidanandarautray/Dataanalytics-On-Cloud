from flask import Flask, render_template, request
import os
import PyPDF2
import re
import pymongo  # Import pymongo

# Set up a MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
db = client["new"]  # Replace with your database name
collection = db["mycollection"]  # Replace with your collection name


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'D:/Flask/Cloud/uploads'

@app.route('/')
def upload_form():
    return render_template('upload_form.html')  # Use just the template name

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

        return render_template('upload_form.html', pdf_text=pdf_text)




@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'file' not in request.files:
        return render_template('upload_form.html', error='No file part')

    file = request.files['file']
    if file.filename == '':
        return render_template('upload_form.html', error='No selected file')

    pdf_text = extract_text_from_pdf(file)
    
   


    return render_template('upload_form.html', pdf_text=pdf_text)

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
if __name__ == '__main__':
    app.run(debug=True) 
