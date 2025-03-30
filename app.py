import webbrowser

from flask import Flask, render_template, request
from fontTools.ttx import process
from werkzeug.utils import secure_filename
import os

from model import process_image

app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)

app.config['UPLOAD'] = upload_folder
process_path = ''



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        process_image(img)
        with open('buffer.txt', 'r') as f:
            process_path = f.readline().strip()
        return render_template('image_render.html', img=img,img1=process_path)
    return render_template('image_render.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    with (open('buffer.txt', 'r') as f):
       f.readline()
       text_file = f.readline().rstrip()
    with  (open(text_file, 'r') as f):
        obj = f.readline()
        clr= f.readline().rstrip()
        webbrowser.open(f'https://yandex.ru/images/search?from=tabbar&text={clr} {obj}')
    return render_template('image_render.html')

if __name__ == '__main__':
    app.run(debug=True, port=8001)