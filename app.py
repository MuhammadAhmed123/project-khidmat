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

@app.route("/registerStudentLink")
def registerStudentLink():
    classes = db.execute("SELECT Class.Name FROM Class")
    return render_template("student_reg.html", classes=classes)

@app.route("/registerStudent", methods=["POST"])
def registerStudent():
    fullName = request.form.get('studentFullName')
    guardianName = request.form.get('studentGuardian')
    emailAddress = request.form.get('studentEmail')
    gender = request.form.get('studentGender')
    religion = request.form.get('studentReligion')
    fathersOccupation = request.form.get('studentFatherOccupation')
    fathersEarning = (request.form.get('studentFatherEarning'))
    mothersOccupation = request.form.get('studentMotherOccupation')
    mothersEarning = (request.form.get('studentMotherEarning'))
    dob = request.form.get('studentdob')
    phoneNumber = request.form.get('studentContact')
    address = request.form.get('studentAddress')
    lastAttendedSchool = request.form.get('studentLastSchool')
    lastAttendedSchoolFees = request.form.get('schoolLastSchoolFee')
    studentClass = request.form.get('studentClass')
    interviewDate = request.form.get('studentInterviewDate')
    testDate = request.form.get('studentAdmissionTestDate')
    uniformMeasurements = request.form.get('studentUniformMeasurement')
    unifromFees = (request.form.get('studentUniformFees'))
    campus = request.form.get('studentCampus')
    shift = request.form.get('shift')
    siblings = request.form.get('studentSiblings')
    sponsorID = None

    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    ID = fullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)
    db.execute("INSERT INTO Person(ID, Name, GuardianName, Gender, Contact, Address, DOB, Campus, Email) VALUES (:ID, :Name, :GuardianName, :Gender, :Contact, :Address, :DOB, :Campus, :Email)",
                {"ID":ID, "Name":fullName, 'GuardianName':guardianName, "Gender":gender, "Contact":phoneNumber, "Address":address, "DOB":dob, "Campus":campus, "Email":emailAddress})

    personID = (list(db.execute("SELECT Person.idPerson FROM Person WHERE Person.ID=:ID", {"ID":ID})))[0][0]
    classID = (list(db.execute("SELECT Class.idClass FROM Class WHERE Class.Name=:studentClass", {"studentClass":studentClass})))[0][0]
    db.execute("INSERT INTO Student(Person_idPerson, Sponsor_Person_idPerson, Class_idClass, Religion, LastAttendedSchool, LastAttendedSchoolFee, Shift, TestDate, InterviewDate, FathersOcuupation, FathersEarning, MothersOccupation, MothersEarning, UniformMeasurement, UniformFees, NoOfSiblings) VALUES (:personID, :sponsorID, :class, :religion, :lastAttendedSchool, :lastAttendedSchoolFees, :shift, :testDate, :interviewDate, :fathersOccupation, :fathersEarning, :mothersOccupation, :mothersEarning, :uniformMeasurements, :unifromFees, :siblings)", {"personID":personID, "sponsorID":sponsorID, "class":classID, "religion":religion, "lastAttendedSchool":lastAttendedSchool, "lastAttendedSchoolFees":lastAttendedSchoolFees, "shift":shift, "testDate":testDate, "interviewDate":interviewDate, "fathersOccupation":fathersOccupation, "fathersEarning":fathersEarning, "mothersOccupation":mothersOccupation, "mothersEarning":mothersEarning, "uniformMeasurements":uniformMeasurements, "unifromFees":unifromFees, "siblings":siblings})
    db.commit()

    return redirect(url_for('registerStudentLink'))

@app.route("/registerStaffLink")
def registerStaffLink():
    return render_template("staff_reg.html")

@app.route("/registerStaff", methods=["POST"])
def registerStaff():
    fullName = request.form.get('staffFullName')
    guardianName = request.form.get('staffGuardianName')
    emailAddress = request.form.get('staffEmailAddress')
    address = request.form.get('staffAddress')
    gender = request.form.get('staffGender')
    dob = request.form.get('staffDob')
    religion = request.form.get('staffReligion')
    staffCategory = request.form.get('staffCategory')
    salary = request.form.get('staffSalary')
    joiningDate = request.form.get('staffJoiningDate')
    qualification = request.form.get('staffQualification')
    campus = request.form.get('staffCampus')
    phoneNumber = request.form.get('staffPhoneNumber')

    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    print(fullName, personCount)
    ID = fullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)

    db.execute("INSERT INTO Person(ID, Name, GuardianName, Gender, Contact, Address, DOB, Campus, Email) VALUES (:ID, :Name, :GuardianName, :Gender, :Contact, :Address, :DOB, :Campus, :Email)",
                {"ID":ID, "Name":fullName, 'GuardianName':guardianName, "Gender":gender, "Contact":phoneNumber, "Address":address, "DOB":dob, "Campus":campus, "Email":emailAddress})
    personID = (list(db.execute("SELECT Person.idPerson FROM Person WHERE Person.ID=:ID", {"ID":ID})))[0][0]
    db.execute("INSERT INTO Staff (Person_idPerson, Salary, Category, joiningDate, Qualification) VALUES (:ID, :Salary, :Category, :joiningDate, :Qualification)",{"ID":personID, "Salary":salary, "Category":staffCategory, "joiningDate":joiningDate, "Qualification":qualification})
    db.commit()

    return redirect(url_for("registerStaffLink"))

@app.route("/registerDonor")
def registerDonor():
    return render_template("donor_reg.html")

@app.route("/registerSponsor")
def registerSponsor():
    return render_template("sponsor_reg.html")


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
