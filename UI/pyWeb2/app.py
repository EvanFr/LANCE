from flask import Flask, request, jsonify, send_file, render_template
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import csv
import json
import base64  # Add this import for Base64 encoding
from PyPDF2 import PdfReader


app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
ANNOTATION_COLOR = {"IoC": [0.90, 0.13, 0.22], "nonIoC": [.42, .85, .16]}  # Define colors
global annotations
time_spent = 0
global OGannotations
annotations = []  # Store annotations for CSV
OGannotations = []
global pdf_path 
pdf_path = None
# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

global messages
messages = []

@app.route('/')
def index():
    return render_template('index.html')


# Initialize globals
context_messages = []
pdf_path = None

@app.route('/get_pdf', methods=['GET'])
def get_pdf():
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False)
    return jsonify({"error": "File not found"}), 404

@app.route('/upload', methods=['POST'])
def upload_pdf():

    global pdf_path
    global annotations
    global OGannotations
    global filename
    """ Upload PDF, render pages, and initialize annotations """
    pdf_file = request.files['file']
    pdf_path = os.path.join(UPLOAD_FOLDER, pdf_file.filename)
    pdf_file.save(pdf_path)

    filename = pdf_file.filename

    pdf = fitz.open(pdf_path)
    pages = []
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Save image in memory to send to frontend as Base64
        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        # Collect page annotations
        page_comments = []
        for annot in page.annots():
            if annot:
                annot_rect = annot.rect
                page_comments.append({
                    "page": page_num,
                    "x0": annot_rect.x0*zoom,
                    "y0": annot_rect.y0*zoom,
                    "x1": annot_rect.x1*zoom,
                    "y1": annot_rect.y1*zoom,
                    "title": annot.info.get('title', 'Untitled'),
                    "label": "Ioc" if annot.colors.get('stroke', [0, 0, 0]) == ANNOTATION_COLOR["IoC"] else "nonIoc",
                    "content": annot.info.get('content', ''),
                    "color": annot.colors.get('stroke', [0, 0, 0]),  # Initial color
                    "reply": []  # Add reply field
                })
                annotations.append(page_comments[-1])  # Track annotations globally for CSV

        pages.append({
            "id": f"page_{page_num}",
            "image": f"data:image/png;base64,{img_base64}",
            "width": pix.width*zoom,
            "height": pix.height*zoom,
            "comments": page_comments
        })

    pdf.close()

    OGannotations = annotations.copy()


    

    return jsonify({"pages": pages})

@app.route('/load_pdf', methods=['POST'])
def load_pdf():
    global pdf_path, annotations, OGannotations, filename

    data = request.json
    selected_pdf = data.get('pdf_name')
    if not selected_pdf:
        return jsonify({"error": "No PDF name provided"}), 400

    pdf_path = os.path.join(UPLOAD_FOLDER, selected_pdf)
    filename = selected_pdf

    pdf = fitz.open(pdf_path)
    pages = []
    annotations = []  # Reset annotations for the new PDF
    for page_num in range(len(pdf)):
        page = pdf[page_num]
        zoom = 2.0
        mat = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        page_comments = []
        for annot in page.annots():
            if annot:
                annot_rect = annot.rect
                page_comments.append({
                    "page": page_num,
                    "x0": annot_rect.x0*zoom,
                    "y0": annot_rect.y0*zoom,
                    "x1": annot_rect.x1*zoom,
                    "y1": annot_rect.y1*zoom,
                    "title": annot.info.get('title', 'Untitled'),
                    "label": "IoC" if annot.colors.get('stroke', [0, 0, 0]) == ANNOTATION_COLOR["IoC"] else "nonIoC",
                    "content": annot.info.get('content', ''),
                    "color": annot.colors.get('stroke', [0, 0, 0]),
                    "reply": []
                })
                annotations.append(page_comments[-1])

        pages.append({
            "id": f"page_{page_num}",
            "image": f"data:image/png;base64,{img_base64}",
            "width": pix.width*zoom,
            "height": pix.height*zoom,
            "comments": page_comments
        })

    pdf.close()
    OGannotations = annotations.copy()

    return jsonify({"pages": pages})


@app.route('/get_pdf_text', methods=['GET'])
def get_pdf_text():
    global pdf_path  
    try:
        reader = PdfReader(pdf_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text, 200
    except Exception as e:
        return str(e), 500

@app.route('/annotations', methods=['GET'])
def get_annotations():
    global annotations
    """ Fetch all annotations to display on frontend """
    return jsonify({"annotations": annotations})

@app.route('/toggle_annotation', methods=['POST'])
def toggle_annotation():
    global annotations
    """ Toggle annotation color based on request """
    data = request.json
    title = data.get("title")
    label_type = data.get("label")  # Either 'IoC' or 'nonIoC'

    # Find and update annotations with matching title
    for annot in annotations:
        if annot["title"] == title:
            annot["color"] = ANNOTATION_COLOR.get(label_type, [0, 0, 0])
            annot["label"] = label_type

    return jsonify({"status": "success", "annotations": annotations})

@app.route('/add_reply', methods=['POST'])
def add_reply():
    global annotations
    data = request.json
    title = data.get('title')
    reply = data.get('reply')

    for annot in annotations:
        if annot["title"] == title:
            annot["reply"].append(reply)

    # Update the comment data with the new reply
    # Here you should update your data structure or database with the reply
    # (for this example, we'll assume you store comments in-memory or update your PDF annotations accordingly)
    
    # Respond with success
    return jsonify(success=True)


@app.route('/download_csv', methods=['GET'])
def download_csv():
    global annotations
    """ Create CSV with annotations and send it to download """
    csv_path = os.path.join(UPLOAD_FOLDER, filename+"_annotations.csv")
    with open(csv_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["title", "label", "content","reply"])
        writer.writeheader()
        for annot in annotations:
            label = "IoC" if annot["color"] == ANNOTATION_COLOR["IoC"] else "nonIoC"
            writer.writerow({
                "title": annot["title"],
                "label": annot["label"],
                "content": annot["content"],
                "reply": annot["reply"]
            })

    return send_file(csv_path, as_attachment=True)

@app.route('/update_time_spent', methods=['POST'])
def update_time_spent():
    global time_spent 

    data = request.json
    time_spent = data.get('time_spent')
    if time_spent:
        return jsonify({'message': 'Time updated successfully'}), 200
    else:
        return jsonify({'error': 'PDF name is required'}), 400

@app.route('/download_json', methods=['GET'])
def download_json():
    global annotations
    global time_spent
    """ Create JSON with annotations and send it to download """
    json_path = os.path.join(UPLOAD_FOLDER, filename+"_annotations.json")
    print(time_spent)
    data = {"annotations": annotations, "time": time_spent}
    with open(json_path, mode='w') as json_file:
        json.dump(data, json_file, indent=4)

    return send_file(json_path, as_attachment=True)

@app.route('/list_pdfs', methods=['GET'])
def list_pdfs():
    pdf_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.pdf')]
    return jsonify(pdf_files)

if __name__ == "__main__":
    app.run(debug=True)

