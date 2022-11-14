from flask import Flask, render_template
import sqlite3 as sql
app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True
db = sql.connect("Video.db")
cursor = db.execute("SELECT * FROM video")
for row in cursor:
    print(row)


@app.route("/")
def index():
    version = 0.60
    return render_template("index.html",version=version)

@app.route("/Web/<subject>")
def Web(subject):
    return render_template("Web/"+subject+".html")

@app.route("/search",methods=["POST"])
def search():
    print("Helloword")




if __name__ == "__main__":
  app.run(host='0.0.0.0')