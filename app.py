from flask import Flask, render_template, request, session, redirect
import sqlite3 as sql
import subprocess as process
import os
from tempfile import mkdtemp
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
con = sql.connect("video.db", check_same_thread=False)
user = sql.connect("user.db", check_same_thread=False)
db = con.cursor()
userdb = user.cursor()
def execute(dbs,command):
    dbs.execute(command)
    con.commit()
    return list(db.fetchall())

converting = []
version = 56

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
    table = execute(db,"SELECT * FROM video")
    return render_template("index.html",version=version,table=table)

@app.route("/Web/<subject>")
@login_required
def Web(subject):
    return render_template("Web/"+subject+".html",version=version)

@app.route("/upload",methods=["GET","POST"])
@login_required
def upload():
    if request.method == "POST":
        if request.form.get("password") == "m101":
            return redirect("http://170.187.225.114:3000")
        else:
            return redirect("/")
    else:
        return render_template("upload.html")

@app.route("/uploads")
@login_required
def uploads():
    return render_template("uploads.html")

@app.route("/search",methods=["GET"])
@login_required
def search():
    args = request.args
    keywords = args.get("search")
    print(keywords)
    related = execute(db,f"SELECT * FROM video WHERE tag LIKE '%{keywords}%'")
    return render_template("search.html",related=related,version=version)

@app.route("/video",methods=["GET"])
@login_required
def video():
    args = request.args
    subject = args.get("subject")
    date = args.get("date")
    link = "http://170.187.225.114:3001/Video/"+subject+"/"+date
    return render_template("video.html",link=link,version=version)

@app.route("/tag/<subject_tag>",methods=["POST","GET"])
@login_required
def tag(subject_tag):
    if request.method == "GET":
        table = execute(db,f"SELECT * FROM video WHERE subject ='{subject_tag}'")
        return render_template("tag.html",table=table,version=version,path=f"/tag/{subject_tag}")
    elif request.method == "POST":
        tag = request.form.get("tag")
        video_id = request.form.get("id")
        execute(db,f"UPDATE video SET tag ='{tag}' WHERE video_id = {video_id}")
        return redirect(f"/tag/{subject_tag}")

@app.route("/tag")
@login_required
def tagpage():
    return render_template("tagmenu.html",version=version)


@app.route("/login",methods=["GET","POST"])
def login():
    session.clear()
    if request.method == "POST":
        continue
    else:
        return render_template("login.html",version=version)

if __name__ == "__main__":
  app.run(host='0.0.0.0')