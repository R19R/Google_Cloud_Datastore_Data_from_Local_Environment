from flask import Flask, json, redirect, render_template, request, jsonify, session, flash
from flask_login.utils import confirm_login
from google.cloud.datastore_v1.proto.entity_pb2 import ArrayValue
from google.cloud.ndb import key
from google.cloud.ndb.model import Key, User
from models import User_Details, db, load_user, login
from flask_login import login_required, current_user, login_user, logout_user
import uuid, csv, os.path
from google.cloud import datastore, ndb



credentials_path = "F:\Google Cloud\Service_datastore.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


db = ndb.Client()


app=Flask(__name__)

app.config['SECRET_KEY']='xyz'

@app.route('/')
def home():
    return render_template('spa.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    with db.context():
        if request.method == "POST":
            log = request.get_json(force=True)
            uname = log.get('name')
            pword = log.get('password')
            session['user'] = uname
            key = ndb.Key(User_Details, uname)
            user_login = User_Details.get_by_id(uname)
            if user_login.username == None:
                return "No User"
            elif user_login.username is not None and (user_login.password == pword):
                return "Login successful!"
            else:
                return "Wrong Credentials"
        return redirect("/")


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    with db.context():
        if request.method == "POST":
            new_user = request.get_json(force=True)
            username = new_user.get('name')
            password = new_user.get('password')
            con_password = new_user.get('confirm_pword')
            filename = "newfile_"+ username + ".csv"
            # id = "id_"+ username
            print(username, password, filename)
            user = User_Details(id=username,username=username, filename=filename, password=password)
            user.set_password(password)
            with open(filename, 'a') as wfile:
                writer = csv.writer(wfile, lineterminator = '\n')
            user.put()    
            return "User Created!"
        return "Method is GET"


@app.route('/logout')
def logout():
    if "user" in session:
        user = session['user']
        flash(f"You have been logged out, {user}", "info")
    session.pop("user", None)
    return redirect('/')


@app.route("/comments", methods=['GET', 'POST'])
def comments():
    f = session.get('user')
    
    filename = "newfile_"+ str(f) +".csv"

    det=[]

    if request.method == 'POST':
        fields = ["UID", "Name", "Comment"]
        params = request.get_json(force=True)
        name_r= params.get('name')
        comments_r = params.get('comment')
        uid = uuid.uuid4()
        with open(filename, 'a') as wfile:
            writer = csv.writer(wfile, lineterminator = '\n') 
            file_is_empty = os.stat(filename).st_size == 0
            if file_is_empty:
                writer.writerow(fields)
            writer.writerow([uid, name_r, comments_r])
        return jsonify({"UID":uid, "name":name_r, "comment":comments_r})
    else:
        with open(filename, 'r') as rfile:
            reader = csv.DictReader(rfile)
            for row in reader:
                detail = dict(row)
                det.append(detail)
            return jsonify(det)
        

if __name__ == "__main__":
    app.run(debug=True)