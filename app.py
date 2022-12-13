from flask import Flask, render_template, request, session, redirect
import sqlite3 as sql
import subprocess as process
import os
app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True
con = sql.connect("video.db")
db = con.cursor()
def execute(dbs,command):
    dbs.execute(command)
    con.commit()
    return list(db.fetchall())

version = 56

#print(execute(db,"SELECT * FROM video"))
@app.route("/")
def index():
    table = execute(db,"SELECT * FROM video")
    return render_template("index.html",version=version,table=table)

@app.route("/Web/<subject>")
def Web(subject):
    return render_template("Web/"+subject+".html",version=version)

@app.route("/upload",methods=["GET","POST"])
def upload():
    if request.method == "POST":
        if request.form.get("password") == "m101":
            return redirect("http://170.187.225.114:3000")
        else:
            return redirect("/")
    else:
        return render_template("upload.html")

@app.route("/uploads")
def uploads():
    return render_template("uploads.html")

@app.route("/search",methods=["GET"])
def search():
    args = request.args
    keywords = args.get("search")
    print(keywords)
    return render_template("search.html")

@app.route("/video",methods=["GET"])
def video():
    args = request.args
    subject = args.get("subject")
    date = args.get("date")
    link = "http://170.187.225.114:3001/Video/"+subject+"/"+date
    return render_template("video.html",link=link)

@app.route("/tag/<subject_tag>",methods=["POST","GET"])
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
def tagpage():
    return render_template("tagmenu.html")

@app.route("/convert")
def convert():
    return render_template("convert.html")

if __name__ == "__main__":
  app.run(host='0.0.0.0')