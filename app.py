from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("mysql://root:@127.0.0.1/tgsapplication")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return render_template("index.html")

# this registration code has to be edited

editRegNames = []
editRegIDs = []

@app.route("/registerEdit")
def registerEdit():
    return render_template("edit_reg.html", names=editRegNames, ids=editRegIDs)

@app.route("/editRegSelectPopulate")
def editRegSelectPopulate(selectValue):
    global editRegNames
    global editRegIDs
    print("value -> ", selectValue)
    if selectValue=="3":
        editRegNames = db.execute("SELECT Person.Name FROM Person WHERE Person.idPerson=Staff.Person_idPerson")
        editRegIDs = db.execute("SELECT Person.ID FROM Person WHERE Person.idPerson=Staff.Person_idPerson")        
    return render_template("edit_reg.html", names=editRegNames, ids=editRegIDs)

@app.route("/viewProfiles")
def viewProfiles():
    data = []
    mode = {"Student": False, "Staff": False, "Sponsor": False, "Donor": False}
    return render_template("viewProfiles.html", data=data, mode=mode)

@app.route("/viewProfileSearchFunction")
def viewProfileSearchFunction():
    data = []
    mode = {"Student": False, "Staff": False, "Sponsor": False, "Donor": False}
    category = request.form.get('viewProfileSearchCategory')
    if category == "1":
        mode['Student']=True
    elif category == "2":
        mode["Staff"]=True
    elif category == "3":
        mode["Sponsor"]=True
    else:
        mode["Donor"]=True
    data = db.execute("SELECT * FROM Person,Student")
    return render_template("viewProfiles.html", data=data, mode=mode)


@app.route("/registerStudentLink")
def registerStudentLink():
    classes = db.execute("SELECT Class.Name FROM Class")
    return render_template("registerStudent.html", classes=classes)

@app.route("/registerStudent", methods=["POST"])
def registerStudent():
    fullName = request.form.get('studentFullName')
    guardianName = request.form.get('studentGuardian')
    emailAddress = request.form.get('studentEmail')
    gender = request.form.get('studentGender')
    religion = request.form.get('studentReligion')
    fatherOccupation = request.form.get('studentFatherOccupation')
    fatherEarning = request.form.get('studentFatherEarning')
    motherOccupation = request.form.get('studentMotherOccupation')
    motherEarning = request.form.get('studentMotherEarning')
    dob = request.form.get('studentdob')
    contact = request.form.get('studentContact')
    address = request.form.get('studentAddress')
    lastAttendedSchool = request.form.get('studentLastSchool')
    lastAttendedSchoolFees = request.form.get('schoolLastSchoolFee')
    studentClass = request.form.get('studentClass')
    interviewDate = request.form.get('studentInterviewDate')
    AdmissionTestDate = request.form.get('studentAdmissionTestDate')
    uniformMeasurements = request.form.get('studentUniformMeasurement')
    unifromFees = request.form.get('studentUniformFees')
    campus = request.form.get('studentCampus')
    siblings = request.form.get('studentSiblings')

    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    ID = fullName[0].lower() + format(personCount, '05d')
    db.execute("INSERT INTO Person(ID, Name, GuardianName, Gender, Contact, Address, DOB, Campus) VALUES (:ID, :Name, :GuardianName, :Gender, :Contact, :Address, :DOB, :Campus)",
                {"ID":ID, "Name":fullName, 'GuardianName':guardianName, "Gender":gender, "Contact":contact, "Address":address, "DOB":dob, "Campus":campus})
    db.commit()


    return redirect(url_for('registerStudentLink'))

@app.route("/registerStaffLink")
def registerStaffLink():
    return render_template("registerStaff.html")

@app.route("/registerStaff", methods=["POST"])
def registerStaff():
    return redirect(url_for('registerStaffLink'))

# below code is running

@app.route("/classLink")
def classLink():
    classes = db.execute("SELECT Class.Name FROM Class")
    return render_template("class.html", classes=classes)

@app.route("/editClass", methods=["POST"])
def editClass():
    existingClass = request.form.get('existingClasses')
    idExistingClass = (list(db.execute("SELECT idClass FROM Class WHERE Class.Name = :className",{"className":existingClass})))[0][0]
    newClass = request.form.get('classEdited')
    db.execute("UPDATE Class SET Class.Name = :newclass WHERE Class.idClass = :id", {"newclass":newClass, "id":int(idExistingClass)})
    db.commit()
    return redirect(url_for('classLink'))

@app.route("/addClass", methods=["POST"])
def addClass():
    addClassName = request.form.get('className')

    classes = db.execute("SELECT Class.Name FROM Class")
    for i in classes:
        if i.Name==addClassName:
            return redirect(url_for('classLink'))   #make a separate page for displaying a warning

    db.execute("INSERT INTO Class(Name) VALUES (:name)",{"name":addClassName})
    db.commit()
    return redirect(url_for('classLink'))

if __name__ == "__main__":
    app.run(debug=True)
