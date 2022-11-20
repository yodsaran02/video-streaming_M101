from flask import Flask, render_template
import sqlite3 as sql
app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True



@app.route("/")
def index():
    version = 0.61
    return render_template("index.html",version=version)

@app.route("/Web/<subject>")
def Web(subject):
    return render_template("Web/"+subject+".html")

@app.route("/search",methods=["GET","POST"])
def search():
    #print("Searching....")
    return render_template("search.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")



if __name__ == "__main__":
  app.run(host='0.0.0.0')