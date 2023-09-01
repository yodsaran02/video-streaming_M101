from flask import Flask, render_template, request, session, redirect
import sqlite3 as sql
import subprocess as process
import os
import requests
from tempfile import mkdtemp
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import date
from login import login_required, lookup, usd

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
online_mode = True
try:
    ip = requests.get('https://api.ipify.org').content.decode('utf8')
except:
    online_mode = False
    ip = "Jwind.tv"

if os.path.exists("./video.db"):
    have_db = True
    have_table = True
else:
    have_db = False
    have_table = False


if have_db:
    con = sql.connect("video.db",check_same_thread=False)
    db = con.cursor()
    def execute(dbs,command):
        dbs.execute(command)
        con.commit()
        return list(db.fetchall())
    try:
        table = execute(db,"SELECT * FROM video")
    except:
        have_table = False

version = 62

def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


#print(execute(db,"SELECT * FROM video"))
@app.route("/")
@login_required
def index():
    if have_table:
        video_count = str(execute(db,"SELECT count(*) FROM video")[0][0])
    else:
        video_count = "Not connected to db"
    return render_template("index.html",version=version,have_db=have_db,have_table=have_table,online_mode=online_mode,video_count=video_count)

@app.route("/Web/<subject>")
@login_required
def Web(subject):
    return render_template("Web/"+subject+".html",version=version,have_db=have_db,have_table=have_table,online_mode=online_mode)

@app.route("/upload",methods=["GET","POST"])
@login_required
def upload():
    if request.method == "POST":
        if request.form.get("password") == "m101":
            return redirect("http://"+ip+":3000")
        else:
            return redirect("/")
    else:
        return render_template("upload.html",have_db=have_db,have_table=have_table,online_mode=online_mode)

@app.route("/uploads")
@login_required
def uploads():
    return render_template("uploads.html",have_db=have_db,have_table=have_table,online_mode=online_mode)

@app.route("/search",methods=["GET"])
@login_required
def search():
    if have_db and have_table:
        args = request.args
        keywords = args.get("search")
        subject_arg = args.get("subject")
        if keywords == None:
            print(subject_arg)
            related = execute(db,f"SELECT * FROM video WHERE subject = '{subject_arg}'")
            return render_template("search.html",related=related,length=len(related),version=version,have_db=have_db,have_table=have_table,online_mode=online_mode)
        else:
            print(keywords)
            related = execute(db,f"SELECT * FROM video WHERE tag LIKE '%{keywords}%'")
            return render_template("search.html",related=related,length=len(related),version=version,have_db=have_db,have_table=have_table,online_mode=online_mode)
    else:
        return render_template("404.html",status_code="Database error")

@app.route("/video",methods=["GET"])
@login_required
def video():
    args = request.args
    subject = args.get("subject")
    date = args.get("date")
    link = "https://jwind.tv:3001/Video/"+subject+"/"+date
    return render_template("video.html",link=link,version=version,have_db=have_db,have_table=have_table,online_mode=online_mode)

@app.route("/tag/<subject_tag>",methods=["POST","GET"])
@login_required
def tag(subject_tag):
    if have_db and have_table:
        if request.method == "GET":
            table = execute(db,f"SELECT * FROM video WHERE subject ='{subject_tag}'")
            return render_template("tag.html",table=table,version=version,path=f"/tag/{subject_tag}",have_db=have_db,have_table=have_table,online_mode=online_mode)
        elif request.method == "POST":
            tag = request.form.get("tag")
            video_id = request.form.get("id")
            execute(db,f"UPDATE video SET tag ='{tag}' WHERE video_id = {video_id}")
            return redirect(f"/tag/{subject_tag}")
    else:
        return render_template("404.html",status_code="Database error")

@app.route("/tag")
@login_required
def tagpage():
    return render_template("tagmenu.html",version=version,have_db=have_db,have_table=have_table,online_mode=online_mode)

@app.route("/login",methods=["POST","GET"])
@login_required
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html")
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["name"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html',status_code=404)

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html',status_code=500)

if __name__ == "__main__":
  app.run(host='0.0.0.0')
