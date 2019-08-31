from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("mysql://root:@localhost/tgsapp")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registerStudent")
def registerStudent():
    return render_template("registerStudent.html")

@app.route("/registerStaff")
def registerStaff():
    return render_template("registerStaff.html")

if __name__ == "__main__":
    app.run(debug=True)
