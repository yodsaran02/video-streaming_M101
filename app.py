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
    return list(db.fetchall())

subject = ["Math","Science","Health","History","English","Social","Thai"]
videos = []
for i in range(7):
    video = os.listdir("/home/Video/"+subject[i])
    videos.append(video)

print(videos)
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
    #print("search")
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

@app.route("/tag",methods=["POST","GET"])
def tag():
    if request.method == "GET":
        table = execute(db,"SELECT * FROM video")
        return render_template("tag.html",table=table,version=version)
    else:
        execute(db,"UPDATE video SET tag ='"+request.form.get("tag")+"' WHERE video_id = "+request.form.get("id")+";")
        print("added")
if __name__ == "__main__":
  app.run(host='0.0.0.0')