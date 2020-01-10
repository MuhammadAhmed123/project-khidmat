from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("mysql://root:@127.0.0.1/tgsapplication")
db = scoped_session(sessionmaker(bind=engine))

#
# @app.route("/loginLink")
# def loginLink():
#     return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if (username == "Admin@gmail.com" and password == "Admin"):
        return redirect(url_for("registerStudentLink"))
    flash("Invalid!")
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("login.html")
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
    ID = fullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)

    db.execute("INSERT INTO Person(ID, Name, GuardianName, Gender, Contact, Address, DOB, Campus, Email) VALUES (:ID, :Name, :GuardianName, :Gender, :Contact, :Address, :DOB, :Campus, :Email)",
                {"ID":ID, "Name":fullName, 'GuardianName':guardianName, "Gender":gender, "Contact":phoneNumber, "Address":address, "DOB":dob, "Campus":campus, "Email":emailAddress})
    personID = (list(db.execute("SELECT Person.idPerson FROM Person WHERE Person.ID=:ID", {"ID":ID})))[0][0]
    db.execute("INSERT INTO Staff (Person_idPerson, Salary, Category, joiningDate, Qualification) VALUES (:ID, :Salary, :Category, :joiningDate, :Qualification)",{"ID":personID, "Salary":salary, "Category":staffCategory, "joiningDate":joiningDate, "Qualification":qualification})
    db.commit()

    return redirect(url_for("registerStaffLink"))


@app.route("/registerDonorLink")
def registerDonorLink():
    return render_template("donor_reg.html")

@app.route("/registerDonor", methods=["POST"])
def registerDonor():
    donorFullName = request.form.get("donorFullName")
    donorGender = request.form.get("donorGender")
    donorEmail = request.form.get("donorEmail")
    donorAddress = request.form.get("donorAddress")
    donorPhoneNumber = request.form.get("donorPhoneNumber")
    donorDOB = request.form.get("donorDOB")
    donorCurrentState = request.form.get("donorCurrentState")
    donorDateDonationStarted = request.form.get("donorDateDonationStarted")
    donorOrganization = request.form.get("donorOrganization")
    donorRemarks = request.form.get("donorRemarks")
    donorGuardianName = "N/A"
    donorCampus = "N/A"

    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    print(donorFullName, personCount)
    ID = donorFullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)

    db.execute("INSERT INTO Person(ID, Name, GuardianName, Gender, Contact, Address, DOB, Campus, Email) VALUES (:ID, :Name, :GuardianName, :Gender, :Contact, :Address, :DOB, :Campus, :Email)",
                {"ID":ID, "Name":donorFullName, 'GuardianName':donorGuardianName, "Gender":donorGender, "Contact":donorPhoneNumber, "Address":donorAddress, "DOB":donorDOB, "Campus":donorCampus, "Email":donorEmail})
    personID = (list(db.execute("SELECT Person.idPerson FROM Person WHERE Person.ID=:ID", {"ID":ID})))[0][0]
    print("personID: ", personID)
    db.execute("INSERT INTO Donor(Person_idPerson, DateDonoationStarted, CurrentState, Organization) VALUES (:ID, :donorDateDonationStarted, :donorCurrentState, :donorOrganization)", {"ID":personID, "donorCurrentState":donorCurrentState, "donorDateDonationStarted":donorDateDonationStarted, "donorOrganization":donorOrganization})
    db.commit()


    return redirect(url_for("registerDonorLink"))

@app.route("/registerSponsorLink")
def registerSponsorLink():
    return render_template("sponsor_reg.html")

@app.route("/registerSponsor", methods=["POST"])
def registerSponsor():
    sponsorFullName = request.form.get("sponsorFullName")
    sponsorGender = request.form.get("sponsorGender")
    sponsorEmail = request.form.get("sponsorEmail")
    sponsorAddress = request.form.get("sponsorAddress")
    sponsorPhoneNumber = request.form.get("sponsorPhoneNumber")
    sponsorDOB = request.form.get("sponsorDOB")
    sponsorCurrentState = request.form.get("sponsorCurrentState")
    sponsorDateSponsorshipDue = request.form.get("sponsorDateSponsorshipDue")
    sponsorDateSponsorshipStart = request.form.get("sponsorDateSponsorshipStart")
    sponsorRemarks = request.form.get("sponsorRemarks")
    sponsorGuardianName = "N/A"
    sponsorCampus = "N/A"

    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    print(sponsorFullName, personCount)
    ID = sponsorFullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)

    db.execute("INSERT INTO Person(ID, Name, GuardianName, Gender, Contact, Address, DOB, Campus, Email) VALUES (:ID, :Name, :GuardianName, :Gender, :Contact, :Address, :DOB, :Campus, :Email)",
                {"ID":ID, "Name":sponsorFullName, 'GuardianName':sponsorGuardianName, "Gender":sponsorGender, "Contact":sponsorPhoneNumber, "Address":sponsorAddress, "DOB":sponsorDOB, "Campus":sponsorCampus, "Email":sponsorEmail})
    personID = (list(db.execute("SELECT Person.idPerson FROM Person WHERE Person.ID=:ID", {"ID":ID})))[0][0]
    print("personID: ", personID)
    db.execute("INSERT INTO Sponsor(Person_idPerson, CurrentState, DateSponsorshipDue, Remarks, DateSponsorshipStarted) VALUES (:ID, :CurrentState, :sponsorDateSponsorshipDue, :sponsorRemarks, :sponsorDateSponsorshipStart)", {"ID":personID, "CurrentState":sponsorCurrentState, "sponsorDateSponsorshipDue":sponsorDateSponsorshipDue, "sponsorRemarks":sponsorRemarks, "sponsorDateSponsorshipStart":sponsorDateSponsorshipStart})
    db.commit()


    return redirect(url_for("registerSponsorLink"))


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


@app.route("/viewProfilesPage")
def viewProfilesPage():
    mode = {'Student': False, 'Staff': False, 'Sponsor': False, 'Donor': False}
    return render_template("viewProfiles.html", mode=mode, data={})

@app.route("/viewFinance")
def viewFinance():
    return render_template("finance.html")


@app.route("/viewFinanceEntry")
def viewFinanceEntry():
    return render_template("financeEntry.html")


@app.route("/viewFinanceItem")
def viewFinanceItem():
    return render_template("financeItem.html")

@app.route("/viewAttendance")
def viewAttendance():
    return render_template("Attendance.html")

@app.route("/viewMarkAttendance")
def viewMarkAttendance():
    return render_template("MarkAttendance.html")


@app.route("/MaintenanceEntryLink")
def MaintenanceEntryLink():
    return render_template("MaintenanceEntry.html")

@app.route("/MaintenanceCategoryLink")
def MaintenanceCategoryLink():
    return render_template("MaintenanceCategory.html")


@app.route("/MaintenanceViewLink")
def MaintenanceViewLink():
    return render_template("MaintenanceActivity.html")

@app.route("/viewTestPage")
def viewTestPage():
    return render_template("Test.html")

if __name__ == "__main__":
    app.run(debug=True)
