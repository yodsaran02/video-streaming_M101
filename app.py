from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/Web/<subject>")
def Web(subject):
    return render_template("Web/"+subject+".html")

if __name__ == "__main__":
  app.run()