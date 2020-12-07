from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
import os
UPLOAD_FOLDER = 'object_detection/image1'
p="hello"
q="hello1"
a=1.00

def read_from_database():
    conn=sqlite3.connect('acc')
    c=conn.cursor()
    c.execute('SELECT * FROM cement_bags')
    data = c.fetchall()
    for row in data:
        print(row)
    c.close()
    conn.close()
    return data

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

app=Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/display_tables')
def display_tables():
    data=read_from_database()
    return render_template('display_tables.html',data=data)

@app.route('/')
def home():
    return render_template('page1.html')

@app.route('/uploadImg',methods=['GET','POST'])
def landing():
    global p
    global a

    if(request.method=="POST"):
        a=float(request.form["thresh"])
        uploaded_files = request.files.getlist("f1[]")
        filenames=[]
        for f in uploaded_files:
            filenames.append(f.filename)
        print(filenames)
        if 'f1' not in request.files:
            return redirect(request.url)
        file = request.files['f1[]'][0]
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print("No2")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            p='object_detection/image1/'+filename
            return redirect(url_for('result'))

    return render_template('image.html')

@app.route('/result')
def result():
    global p
    global q
    global a
    q="static/"+p[24:-5]+"_result"+p[-5:]
    from obj3 import get_image
    a1,r=get_image(a,p,q)
    return render_template('imagepredict.html',q=r,c=a1)

if __name__=='__main__':
    app.run(debug=True)
