from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
import os
from sqlite3 import *
from datetime import datetime as time
import sqlite3
import cv2
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'intern.1mway@gmail.com'
app.config['MAIL_PASSWORD'] = 'karankamdar'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
UPLOAD_FOLDER = 'object_detection/image1'
p=[]
q=[]
a=1.00
status=0
aes=0
def read_from_database():
    conn=connect('acc')
    c=conn.cursor()
    c.execute('SELECT * FROM cement_bags ORDER BY stack_number DESC;')
    data = c.fetchall()
    for row in data:
        print(row)
    c.close()
    conn.close()
    return data

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/feedback')
def feeback():
    return render_template('feedback.html')

@app.route('/uploadImg',methods=['GET','POST'])
def landing():
    global p
    global a
    if(request.method=="POST"):
        a=float(request.form["thresh"])
        if 'f1' not in request.files:
            return redirect(request.url)
        #file = request.files['f1']
        uploaded_files = request.files.getlist("f1")
        if(len(uploaded_files)!=2):
            return render_template('image.html')
        for i in range(len(uploaded_files)):
        # if user does not select file, browser also
        # submit a empty part without filename
            if uploaded_files[i].filename == '':
                print("No2")
                return redirect(request.url)
            if uploaded_files[i] and allowed_file(uploaded_files[i].filename):
                filename = secure_filename(uploaded_files[i].filename)
                uploaded_files[i].save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                p.append('object_detection/image1/'+filename)
        return redirect(url_for('result'))

    return render_template('image.html')

@app.route('/result')
def result():
    global p
    global q
    global a
    for i in range(len(p)):
        s=p[i]
        q.append("static/"+s[24:-5]+"_result"+s[-5:])
    from obj5 import rec
    #a0,r0=get_image(p[0],q[0],a)
    #a1,r1=get_image(p[1],q[1],a)
    #a2,r2=get_image(p[2],q[2],a)
    a1=rec(p[0],q[0])
    a2=rec(p[1],q[1])
    #vol=16348945.632118575
   
   
    conn=connect('acc')
    rst=conn.execute('SELECT * FROM cement_bags;')
    rst=rst.fetchall()
    conn.close()
    print(rst)
    lm=len(rst)
    l=rst[lm-1][2]
    l=int(l)
    os.mkdir('static/'+str(l+1))
    from zipfile import ZipFile
    zipObj = ZipFile('static/'+str(l+1)+'/sample.zip', 'w')
    folder_path='static/'+str(l+1)
    
    cv2.imwrite('static/'+str(l+1)+'/'+p[0][24:-5]+"_result"+p[0][-5:],cv2.imread(q[0]))
    cv2.imwrite('static/'+str(l+1)+'/'+p[1][24:-5]+"_result"+p[1][-5:],cv2.imread(q[1]))
    co=0
    for filename in os.listdir(folder_path):
        co+=1
        if(co<3):
            print(os.path.join(folder_path, filename))
            zipObj.write(os.path.join(folder_path, filename))
        else:
            break
    # close the Zip File
    zipObj.close()
    conn=connect('acc')
    conn.execute("INSERT INTO cement_bags(time_stamp, warehouse_location, stack_number, stack_bag_count,stack_location) VALUES (?, ?, ?, ?, ?)",
          (str(time.now()), 'Chembur', int(l+1), a1*a2,'static/'+str(l+1)+'/sample.zip'))
    conn.commit()
    q0=q[0]
    q1=q[1]
    p=[]
    q=[]
    #conn.close()
    return render_template('imagepredict.html',q0=q0,q1=q1,c=str(a1)+' X '+str(a2)+' = '+str(a1*a2))

@app.route('/display_tables')
def display_tables():
    data=read_from_database()
    return render_template('display_tables.html',data=data)

def verify_from_database(username,password):
    global status
    users=dict()
    conn=sqlite3.connect('registration.db')
    c=conn.cursor()
    var=False
    c.execute('SELECT * FROM users')
    data=c.fetchall()
    for row in data:
        users[row[0]]=row[1]
    for key,value in users.items():
        if username == key and password == value:
            var=True
    c.close()
    conn.close()
    return var

def write_to_register(email,passw,full_name,username):
    global aes
    conn = sqlite3.connect('registration.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users(email, pass, full_name, username) VALUES (?, ?, ?, ?)",
              (email, passw, full_name, username))
        print("Written Successfully")
        conn.commit()
        c.close()
        conn.close()
        return redirect(url_for('login'))
    except:
        conn.commit()
        c.close()
        conn.close()
        aes=1
        return redirect(url_for('register'))


@app.route('/login')
def login():
   return render_template("index.html")


@app.route('/feedback')
def feedback():
   return render_template("feedback.html")

@app.route('/resultlogin',methods=['POST','GET'])
def resultlogin():
    global current_user
    if request.method == 'POST':
        res=request.form
        email=res['username']
        passw=res['pass']
        if verify_from_database(email,passw):
            current_user=email
            return redirect(url_for('landing'))
        else:
            return render_template("login_error.html")

@app.route('/register')
def register():
    global aes
    if(aes==1):
        aes=0
        return render_template("reg_error.html")
    return render_template("register.html")

@app.route('/table')
def table():
   return render_template("table.html")

@app.route('/result',methods=['POST','GET'])
def registerresult():
    if request.method == 'POST':
        res=request.form
        print(res)
        print()
        email=res['email']
        print(email)
        passw=res['pass']
        print(passw)
        full_name=res['name']
        username=res['username']
        print("OK")
        return write_to_register(email,passw,full_name,username)

if __name__=='__main__':
    app.run(debug=True)
