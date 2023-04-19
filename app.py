from flask import Flask, render_template, request, send_file
import os
from constants import * 
from prompt_generator import * 
import openai

openai.api_key = OPENAI_KEY

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/process', methods=['POST'])
def process():
    # Get the uploaded file from the request
    file = request.files['inputfile']
    # Save the uploaded file to the UPLOAD_FOLDER
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    text = open(file_path).read()
    text = text.replace(',','')
    # Process the file (placeholder code)
    # TODO: replace this with your own processing code
    processed_data = text_to_table(text,columns=BASELINE_COLUMNS)
    # Save the processed data to a CSV file in the DOWNLOAD_FOLDER
    csv_path = os.path.join('table_to_text.csv')
    print(csv_path)
    print(processed_data.head())
    # Return the path to the CSV file
    return csv_path

@app.route('/download')
def download_file():
    # Replace 'result.csv' with the name of the file you want to download
    filename = 'table_to_text.csv'
    # Replace '/path/to/your/file' with the path to the directory where the file is stored
    file_path = filename
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    
    app.run(debug=True)

