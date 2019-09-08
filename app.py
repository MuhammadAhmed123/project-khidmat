from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("mysql://root:@localhost/tgsapp")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registerStudentLink")
def registerStudentLink():
    classes = db.execute("SELECT class.Name FROM class")
    return render_template("registerStudent.html", classes=classes)

@app.route("/registerStudent", methods=["POST"])
def registerStudent():

    return redirect(url_for('registerStudentLink'))

@app.route("/registerStaffLink")
def registerStaffLink():
    return render_template("registerStaff.html")

@app.route("/registerStaff", methods=["POST"])
def registerStaff():
    return redirect(url_for('registerStaffLink'))

@app.route("/classLink")
def classLink():
    classes = db.execute("SELECT class.Name FROM class")
    return render_template("class.html", classes=classes)

@app.route("/editClass", methods=["POST"])
def editClass():
    existingClass = request.form.get('existingClasses')
    idExistingClass = (list(db.execute("SELECT idClass FROM class WHERE class.Name = :className",{"className":existingClass})))[0][0]
    newClass = request.form.get('classEdited')
    db.execute("UPDATE class SET class.Name = :newclass WHERE class.idClass = :id", {"newclass":newClass, "id":int(idExistingClass)})
    db.commit()
    return redirect(url_for('classLink'))

@app.route("/addClass", methods=["POST"])
def addClass():
    addClassName = request.form.get('className')

    classes = db.execute("SELECT class.Name FROM class")
    for i in classes:
        if i.Name==addClassName:
            return redirect(url_for('classLink'))   #make a separate page for displaying a warning

    db.execute("INSERT INTO class(Name) VALUES (:name)",{"name":addClassName})
    db.commit()
    return redirect(url_for('classLink'))

if __name__ == "__main__":
    app.run(debug=True)
