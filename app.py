from flask import Flask, render_template, request, session, redirect
import sqlite3 as sql
import subprocess as process
import os
app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True
con = sql.connect("video.db")
db = con.cursor()
def execute(db,command):
    db.execute(command)
    return list(db.fetchone())

subject = ["Math","Science","Health","History","English","Social","Thai"]
videos = []
for i in range(7):
    video = os.listdir("/home/Video/"+subject[i])
    videos.append(video)

print(videos)

#print(execute(db,"SELECT * FROM video"))
@app.route("/")
def index():
    version = 56
    return render_template("index.html",version=version)

@app.route("/Web/<subject>")
def Web(subject):
    return render_template("Web/"+subject+".html")

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







if __name__ == "__main__":
  app.run(host='0.0.0.0')