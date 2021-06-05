from flask import Flask, json, redirect, render_template, request, jsonify, session, flash
from flask_login.utils import confirm_login
from models import User_Details, db, load_user, login
from flask_login import login_required, current_user, login_user, logout_user
import uuid, csv, os.path
from google.cloud import datastore, ndb



credentials_path = "F:\Google Cloud\LocalDevelopment.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


db = ndb.Client()


app=Flask(__name__)


@app.route('/')
def home():
    return render_template('spa.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        log = request.get_json(force=True)
        uname = log.get('name')
        pword = log.get('password')
        session['user'] = uname
        with db.context():
            ancestor_key = ndb.Key("User", "user_name")
            user = User_Details.query(ancestor=ancestor_key,username=uname).fetch(1)
            print(user)
        if user == None:
            return "No User"
        elif user is not None and user.check_password(pword):
            login_user(user)
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
            user = User_Details(username=username, filename=filename, password=password)
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