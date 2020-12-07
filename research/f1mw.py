from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
import os
UPLOAD_FOLDER = 'object_detection/image1'
p="hello"
q="hello1"
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/',methods=['GET','POST'])
def landing():
    global p
    if(request.method=="POST"):
        if 'f1' not in request.files:
            return redirect(request.url)
        file = request.files['f1']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print("No2")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            p='object_detection/image1'+filename
            return redirect(url_for('result'))
            
    return render_template('image.html')

@app.route('/result')
def result():
    
    return render_template('imagepredict.html')

if __name__=='__main__':
    app.run(debug=True)
