import os
from flask import Flask, request, render_template_string
from PIL import Image
import easyocr
 
app = Flask(__name__)
 
HTML_TEMPLATE = '''
<!doctype html>
<title>Simple Image OCR Flask ML App (EasyOCR)</title>
<h1>Upload an image</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
{% if image_url %}
  <h2>Uploaded Image:</h2>
  <img src="{{image_url}}" style="max-width:400px;">
  <h2>Extracted Text:</h2>
  <pre>{{text}}</pre>
{% endif %}
'''
 
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
 
# Initialize reader only once for efficiency
reader = easyocr.Reader(['en'])
 
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    image_url = None
    text = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
 
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            image_url = f'/{filepath}'
            # EasyOCR works directly with filepaths
            results = reader.readtext(filepath, detail=0)
            text = "\n".join(results)
    return render_template_string(HTML_TEMPLATE, image_url=image_url, text=text)
 
if __name__ == '__main__':
    app.run(debug=True)
