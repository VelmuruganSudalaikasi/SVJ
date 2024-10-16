from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

# Use the absolute path to the CSV files
DATA_FOLDER = r"data\csv_output"

# Function to load and return data from a specific file
def load_data(topic):
    # Mapping the topic to its respective CSV file
    file_mapping = {
        'Breast Cancer': 'Breast Cancer.csv',  # Ensure file names match exactly
        'Cancer Prevention': 'Cancer Prevention.csv',
        'Cancer survivors': 'Cancer survivors.csv',
        'Cancer': 'Cancer Survivors.csv',
        'Complementary and alternative medicine':'Complementary and alternative medicine.csv',
        'Diagnosis and cancer':'Diagnosis and cancer.csv',
        'Ematology':'Ematology.csv',
        'Environment and cancer':'Environment and cancer.csv',
        'Epidemiology':'Epidemiology.csv',
        'Epigenetic':'Epigenetic.csv',
        'Gastrointestinal cancer':'Gastrointestinal cancer.csv',
        'Genitourinary cancer':'Genitourinary cancer.csv',
        'Geriatric oncology':'Geriatric oncology.csv',
        'Gynaecological cancer':'Gynaecological cancer.csv',
        'Haematological oncology':'Haematological oncology.csv',
        'Head and neck cancer':'Head and neck cancer.csv',
        'HIV and cancer':'HIV and cancer.csv',
        'Immunoncology':'Immunoncology.csv',
        'Lung cancer':'Lung cancer.csv',
        'Medical oncology':'Medical oncology.csv',
        'Microbiota and cancer':'Microbiota and cancer.csv',
        'Molecular diagnosis':'Molecular diagnosis.csv',
        'Nutrition and cancer':'Nutrition and cancer.csv',
        'Otolaryngology':'Otolaryngology.csv',
        'Pediatric oncology and onco-haematology':'Pediatric oncology and onco-haematology.csv',
        'Pharmacoeconomics':'Pharmacoeconomics.csv',
        'Pharmacogenomics':'Pharmacogenomics.csv',
        'Psyco-oncology':'Psyco-oncology.csv',
        'Radiotherapy':'Radiotherapy.csv',
        'Skin cancer':'Skin cancer.csv',
        'Surgical oncology':'Surgical oncology.csv',
        'Translational research':'Translational research.csv',
        'Virus and cancer':'Virus and cancer.csv'
    }
    
    # Construct the absolute file path
    file_path = os.path.join(DATA_FOLDER, file_mapping[topic])

    # Debugging: print the file path to ensure correctness
    print(f"Loading data from: {file_path}")
    
    # Return the loaded CSV data
    return pd.read_csv(file_path)

# Function to generate charts based on the data and selected chart type
def generate_chart(data, chart_type):
    if chart_type == 'Bar':
        fig = px.bar(data, x='Place of research', y='Number of patients', title='Bar Chart: Number of Patients')
    elif chart_type == 'Line':
        fig = px.line(data, x='Year of research', y='Number of patients', title='Line Chart: Number of Patients Over Time')
    elif chart_type == 'Pie':
        fig = px.pie(data, names='Place of research', values='Number of patients', title='Pie Chart: Patients Distribution')
    else:
        fig = px.bar(data, x='Place of research', y='Number of patients', title='Default Bar Chart')

    return fig.to_html(full_html=False)

# Route for the homepage
@app.route("/", methods=['GET', 'POST'])
def index():
    topics = ['Breast Cancer', 'Cancer Prevention','Cancer survivors', 'Cancer','Complementary and alternative medicine','Diagnosis and cancer','Ematology','Environment and cancer','Epidemiology','Epigenetic','Gastrointestinal cancer','Genitourinary cancer','Geriatric oncology','Gynaecological cancer','Haematological oncology','Head and neck cancer','HIV and cancer','Immunoncology','Lung cancer','Medical oncology','Microbiota and cancer','Molecular diagnosis','Nutrition and cancer','Otolaryngology','Pediatric oncology and onco-haematology','Pharmacoeconomics','Pharmacogenomics','Psyco-oncology','Radiotherapy','Skin cancer','Surgical oncology','Translational research','Virus and cancer']  # List of topics for the dropdown
    chart_types = ['Bar', 'Line', 'Pie']  # List of chart types
    
    selected_topic = request.form.get('topic') if request.method == 'POST' else topics[0]
    selected_chart = request.form.get('chart_type') if request.method == 'POST' else chart_types[0]

    data = load_data(selected_topic)
    chart_html = generate_chart(data, selected_chart)
    
    return render_template('index.html', topics=topics, chart_types=chart_types, selected_topic=selected_topic, selected_chart=selected_chart, chart_html=chart_html)

if __name__ == "__main__":
    app.run(debug=True)
