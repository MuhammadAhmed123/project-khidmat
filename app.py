from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
import datetime


# temporary variables
existingEvent = ""
eventEditId = -1
editRegNames = []
editRegIDs = []
vehicleEditId = -1
vehCatToEditId = -1

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

engine = create_engine("mysql://root:@127.0.0.1/tgsapplication")
db = scoped_session(sessionmaker(bind=engine))


#region login module
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if (username == "Admin@gmail.com" and password == "Admin"):
        return redirect(url_for("registerStudentLink"))
    # flash("Invalid!")
    return redirect(url_for("index"))



@app.route("/")
def index():
    return render_template("login.html")
#endregion


#region medical module
@app.route("/hepatitisLink")
def hepatitisLink():
    return render_template("EditHepatitis.html")

@app.route("/hepatitis", methods=["POST"])
def hepatitis():
    return redirect(url_for("hepatitisLink"))


@app.route("/bloodLink")
def bloodLink():
    # st = db.execute("SELECT person.Name FROM person, student WHERE person.idPerson=student.Person_idPerson")
    st = db.execute("SELECT person.ID FROM person, student WHERE person.idPerson=student.Person_idPerson")
    return render_template("EditBlood.html", studentBlood=st )

@app.route("/blood", methods=["POST"])
def blood():
    studentID = request.form.get("studentID")
    bloodTestDate = request.form.get("bloodTestDate")
    bloodGroup = request.form.get("bloodGroup")
    hemoglobinLevels = request.form.get("hemoglobinLevels")
    bloodRemarks = request.form.get("bloodRemarks")

    db.execute()
    db.commit()
    return redirect(url_for("bloodLink"))


@app.route("/typhoidLink")
def typhoidLink():
    return render_template("EditTyphoid.html")

@app.route("/typhoid", methods=["POST"])
def typhoid():
    return redirect(url_for("typhoidLink"))


@app.route("/ENTLink")
def ENTLink():
    return render_template("EditENT.html")

@app.route("/ENT", methods=["POST"])
def ENT():
    return redirect(url_for("ENTLink"))
#endregion


#region AJAX reference code
@app.route("/viewTestAjax")
def viewTestAjax():
    classes = db.execute("SELECT Class.Name FROM Class")
    return render_template("testAjax.html", classes=classes)

@app.route("/getStudentsOfClass", methods=["POST"])
def getStudentsOfClass():
    Class =  request.get_json()['classSelected'] # request.form.get('existingClasses')
    classID = (list(db.execute("SELECT Class.idClass FROM Class WHERE Class.Name=:studentClass", {"studentClass":Class})))[0][0]
    students = list(db.execute("SELECT person.Name FROM person,student WHERE person.idPerson = student.Person_idPerson AND student.Class_idClass = :classID", {'classID':classID}))
    # print(students)
    # # students = []
    # print(Class)
    return jsonify({'data': render_template('response.html',students=students)})
#endregion


#region vehicle module
@app.route("/vehicleMaintenanceLink")
def vehicleMaintenanceLink():
    mainCategories = db.execute("SELECT Name FROM vehiclemaintenancecategory")
    vehicles = db.execute("SELECT Name FROM vehicle")

    return render_template("vehicleMaintenance.html", mainCategories=mainCategories, vehicles=vehicles)


@app.route("/vehMainAdd", methods=["POST"])
def vehMainAdd():

    vehicleName = request.form.get("vehicleName")
    maintenanceCat = request.form.get("maintenanceCat")
    vehId = list(db.execute("SELECT idVehicle FROM vehicle WHERE Name = :vehicleName",{"vehicleName":vehicleName}))[0][0]
    mainCatId = list(db.execute("SELECT idVehicleMaintenanceCategory FROM vehiclemaintenancecategory WHERE Name = :maintenanceCat",{"maintenanceCat":maintenanceCat}))[0][0]
    vehicleMaintenanceDate = request.form.get("vehicleMaintenanceDate")
    vehicleMaintenanceExpense = request.form.get("vehicleMaintenanceExpense")
    vehicleMaintenanceRemarks = request.form.get("vehicleMaintenanceRemarks")

    db.execute("INSERT INTO vehiclemaintenance (VehicleMaintenanceCategory_idVehicleMaintenanceCategory, Vehicle_idVehicle, Expense, Date, Remarks) VALUES (:vehId, :mainCatId, :vehicleMaintenanceExpense, :vehicleMaintenanceDate, :vehicleMaintenanceRemarks)",{"vehId":vehId, "mainCatId":mainCatId, "vehicleMaintenanceExpense":vehicleMaintenanceExpense, "vehicleMaintenanceDate":vehicleMaintenanceDate, "vehicleMaintenanceRemarks":vehicleMaintenanceRemarks})
    db.commit()

    return redirect(url_for("vehicleMaintenanceLink"))


@app.route("/vehicleMaintenanceCat")
def vehicleMaintenaceCat():
    global vehCatToEditId
    categories = db.execute("SELECT Name FROM vehiclemaintenancecategory")
    vehCatCol = list(db.execute("SELECT * FROM vehiclemaintenancecategory WHERE idVehicleMaintenanceCategory = :vehCatToEditId",{"vehCatToEditId":vehCatToEditId}))
    if vehCatCol == [] or vehCatToEditId == -1:
        vehCatCol = [("", "", "")]
    ovcn = vehCatCol[0][1]
    ovcd = vehCatCol[0][2]
    return render_template("vehicleMaintenanceCategory.html", categories=categories, ovcn = ovcn, ovcd = ovcd)

@app.route("/vehicleCatAdd", methods=["POST"])
def vehicleCatAdd():
    vehCatName = request.form.get("vehCatName")
    vehCatDescription = request.form.get("vehCatDescription")

    db.execute("INSERT INTO vehiclemaintenancecategory (Name, Description) VALUES (:vehCatName, :vehCatDescription)",{"vehCatName":vehCatName, "vehCatDescription":vehCatDescription})
    db.commit()
    return redirect(url_for("vehicleMaintenaceCat"))

@app.route("/vehicleCatSearch", methods=["POST"])
def vehicleCatSearch():
    global vehCatToEditId
    vehCatToEdit = request.form.get("vehCatToEdit")
    vehCatToEditId = list(db.execute("SELECT idVehicleMaintenanceCategory FROM vehiclemaintenancecategory WHERE Name = :vehCatToEdit",{"vehCatToEdit":vehCatToEdit}))
    if vehCatToEditId == []:
        vehCatToEditId = -1
    else:
        vehCatToEditId = vehCatToEditId[0][0]

    return redirect(url_for("vehicleMaintenaceCat"))

@app.route("/vehicleCatUpdate", methods=["POST"])
def vehicleCatUpdate():
    global vehCatToEditId

    newVehCatName = request.form.get("newVehCatName")
    newVehCatDes = request.form.get("newVehCatDes")

    if vehCatToEditId != -1:
        db.execute("UPDATE vehiclemaintenancecategory SET Name = :newVehCatName, Description = :newVehCatDes WHERE idVehicleMaintenanceCategory = :vehCatToEditId",{"newVehCatName":newVehCatName, "newVehCatDes":newVehCatDes, "vehCatToEditId":vehCatToEditId})
        db.commit()

    return redirect(url_for("vehicleMaintenaceCat"))



@app.route("/vehicleLink")
def vehicleLink():
    vehicleCol = list(db.execute("SELECT * FROM vehicle WHERE idVehicle = :vehicleEditId",{"vehicleEditId":vehicleEditId}))
    if vehicleEditId == -1 or vehicleCol == []:
        vehicleCol = [("", "", "")]
    ov = vehicleCol[0][1]
    ovrn = vehicleCol[0][2]
    vehicles = db.execute("SELECT Name FROM vehicle")

    return render_template("vehicle.html",vehicles = vehicles , ov = ov, ovrn = ovrn)

@app.route("/vehicleAdd", methods=["POST"])
def vehicleAdd():
    vehicleName = request.form.get("vehicleName")
    vehicleRegistrationNumber = request.form.get("vehicleRegistrationNumber")

    db.execute("INSERT INTO vehicle (Name, RegistrationNumber) VALUES (:Name, :RegistrationNumber)",{"Name":vehicleName, "RegistrationNumber":vehicleRegistrationNumber})
    db.commit()
    return redirect(url_for("vehicleLink"))

@app.route("/vehicleSearch", methods=["POST"])
def vehicleSearch():
    global vehicleEditId
    vehicleToEdit = request.form.get("vehicleToEdit")
    vehicleEditId = list(db.execute("SELECT idVehicle FROM vehicle WHERE Name = :vehicleToEdit",{"vehicleToEdit":vehicleToEdit}))
    if vehicleEditId == []:
        vehicleEditId = -1
    else:
        vehicleEditId = vehicleEditId[0][0]
    return redirect(url_for("vehicleLink"))

@app.route("/vehicleUpdate", methods=["POST"])
def vehicleUpdate():
    print("vehicleEditId 2 : ", vehicleEditId)
    newVehicle = request.form.get("newVehicle")
    newVehicleRegistrationNumber = request.form.get("newVehicleRegistrationNumber")
    if vehicleEditId != -1:
        db.execute("UPDATE vehicle SET Name = :newVehicle, RegistrationNumber = :newVehicleRegistrationNumber WHERE idVehicle = :vehicleEditId",{"newVehicle":newVehicle, "newVehicleRegistrationNumber":newVehicleRegistrationNumber, "vehicleEditId":vehicleEditId})
        db.commit()

    return redirect(url_for("vehicleLink"))

#endregion


#region utility bill module
@app.route("/utilityLink")
def utilityLink():
    return render_template("Utilities.html")

@app.route("/utility", methods=["POST"])
def utility():
    billName = request.form.get("billName")
    billDueDate = request.form.get("billDueDate")
    billAmount = request.form.get("billAmount")
    billPaymentDate = request.form.get("billPaymentDate")
    billRemarks = request.form.get("billRemarks")

    db.execute("INSERT INTO utilitybills (Category, DueDate, PaymentDate, Amount, Remarks) VALUES (:Category, :DueDate, :PaymentDate, :Amount, :Remarks) ",{"Category":billName, "DueDate":billDueDate, "PaymentDate":billPaymentDate, "Amount":billAmount, "Remarks":billRemarks})
    db.commit()
    return redirect(url_for('utilityLink'))

#endregion


#region event module
def dateProcess(date):
    if date == "N/A" or date == "None" or date == "":
        return date
    return (date[5:7]+"-"+date[8:]+"-"+date[0:4])

@app.route("/eventLink")
def eventLink():
    global existingEvent
    events = db.execute("SELECT Name FROM event")
    existingEventCol = list(db.execute("SELECT * FROM event WHERE Name=:existingEvent", {"existingEvent":existingEvent}))
    if existingEvent == "" or existingEvent == []:
        existingEventCol = [(0,"","","","")]
    print("existingEventCol ",existingEventCol)
    oldId = existingEventCol[0][0]
    oldName = existingEventCol[0][1]
    oldDate = dateProcess(str(existingEventCol[0][2]))
    oldBudget = existingEventCol[0][3]
    oldRemarks =  existingEventCol[0][4]
    return render_template("events_information.html", events=events, oldName=oldName, oldDate=oldDate, oldBudget=oldBudget, oldRemarks=oldRemarks)

@app.route("/event", methods=["POST"])
def event():
    eventName = request.form.get("eventName")
    eventDate = request.form.get("eventDate")
    eventBudget = request.form.get("eventBudget")
    eventDetails = request.form.get("eventDetails")

    db.execute("INSERT INTO event (Name, Date, Budget, Remarks) VALUES (:Name, :Date, :Budget, :Remarks) ",{"Name":eventName, "Date":eventDate, "Budget":eventBudget, "Remarks":eventDetails})
    db.commit()
    return redirect(url_for('eventLink'))

@app.route("/eventSearch", methods=["POST"])
def eventSearch():
    global existingEvent
    global eventEditId
    existingEvent = request.form.get("existingEvent")
    eventEditId = list(db.execute("SELECT idEvent FROM event where event.Name = :existingEvent",{"existingEvent":existingEvent}))[0][0]
    return redirect(url_for('eventLink'))

@app.route("/eventEdit", methods=["POST"])
def eventUpdate():
    global eventEditId
    if eventEditId != -1:
        newEventName = request.form.get("newEventName")
        newEventDate = request.form.get("newEventDate")
        newEventBudget = request.form.get("newEventBudget")
        newEventDetails = request.form.get("newEventDetails")
        # print("eventEditId: ", eventEditId)
        db.execute("UPDATE event SET Name = :newEventName, Date = :newEventDate, Budget = :newEventBudget, Remarks = :newEventDetails WHERE idEvent = :eventEditId",{"newEventName":newEventName, "newEventDate":newEventDate, "newEventBudget":newEventBudget, "newEventDetails":newEventDetails, "eventEditId":eventEditId})
        db.commit()
    else:
        pass
        # should show message to select event first.
    events = db.execute("SELECT Name FROM event")
    return render_template("events_information.html", events=events)

#endregion


#region registeration module
def upload(image):
    filename = secure_filename(image.filename)
    if image.filename == "":
        return ""
    target = os.path.join(APP_ROOT, "profileImages/")
    if not os.path.isdir(target):
        os.mkdir(target)

    destination = "/".join([target, filename])
    image.save(destination)
    return destination

@app.route("/registerStudentLink")
def registerStudentLink():
    classes = db.execute("SELECT Class.Name FROM Class")
    return render_template("student_reg.html", classes=classes)

@app.route("/registerStudent", methods=["GET","POST"])
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

    studentTC = request.form.get('studentTC')
    sponsorLetter = request.form.get('sponsorLetter')
    schoolRules = request.form.get('schoolRules')
    currentState = request.form.get('currentState')
    hepatitis = request.form.get('hepatitis')
    studentMedicalFees = request.form.get('studentMedicalFees')
    studentSchoolFees = request.form.get('studentSchoolFees')

    studentImage = request.files['studentImage']
    path = upload(studentImage)

    sponsorID = None

    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    ID = fullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)
    db.execute("INSERT INTO Person(ID, Name, Gender, Contact, Address, Email) VALUES (:ID, :Name, :Gender, :Contact, :Address, :Email)",
                {"ID":ID, "Name":fullName, "Gender":gender, "Contact":phoneNumber, "Address":address, "Email":emailAddress})

    personID = (list(db.execute("SELECT Person.idPerson FROM Person WHERE Person.ID=:ID", {"ID":ID})))[0][0]
    classID = (list(db.execute("SELECT Class.idClass FROM Class WHERE Class.Name=:studentClass", {"studentClass":studentClass})))[0][0]
    db.execute("INSERT INTO Student(Person_idPerson, Sponsor_Person_idPerson, Class_idClass, Religion, LastAttendedSchool, LastAttendedSchoolFee, Shift, TestDate, InterviewDate, FathersOcuupation, FathersEarning, MothersOccupation, MothersEarning, UniformMeasurement, UniformFees, NoOfSiblings, DOB, Campus, GuardianName, TransferLeavingCertificate, SponsorLetter, schoolRules, HealthFees, SchoolFees) VALUES (:personID, :sponsorID, :class, :religion, :lastAttendedSchool, :lastAttendedSchoolFees, :shift, :testDate, :interviewDate, :fathersOccupation, :fathersEarning, :mothersOccupation, :mothersEarning, :uniformMeasurements, :unifromFees, :siblings,  :DOB, :Campus, :GuardianName, :TransferLeavingCertificate, :SponsorLetter, :schoolRules, :HealthFees, :SchoolFees)", {"personID":personID, "sponsorID":sponsorID, "class":classID, "religion":religion, "lastAttendedSchool":lastAttendedSchool, "lastAttendedSchoolFees":lastAttendedSchoolFees, "shift":shift, "testDate":testDate, "interviewDate":interviewDate, "fathersOccupation":fathersOccupation, "fathersEarning":fathersEarning, "mothersOccupation":mothersOccupation, "mothersEarning":mothersEarning, "uniformMeasurements":uniformMeasurements, "unifromFees":unifromFees, "siblings":siblings,  "DOB":dob, "Campus":campus, "GuardianName":guardianName, "TransferLeavingCertificate":studentTC, "SponsorLetter":sponsorLetter, "schoolRules":schoolRules, "HealthFees":studentMedicalFees, "SchoolFees":studentSchoolFees})
    db.execute("INSERT INTO hepatitisrecord (Student_Person_idPerson, HaveHapatitisDose) VALUES (:Student_Person_idPerson, :HaveHepatitisDose)",{"Student_Person_idPerson":personID, "HaveHepatitisDose":hepatitis})
    db.execute("INSERT INTO image (Person_idPerson, Path) VALUES (:Person_idPerson, :Path)",{"Person_idPerson":personID, "Path":path})
    db.commit()


    if True:
        flash('"{}" successfully registered!'.format(fullName))
    return redirect(url_for('registerStudentLink'))

@app.route("/registerStaffLink")
def registerStaffLink():
    return render_template("staff_reg.html")

@app.route("/registerStaff", methods=["POST"])
def registerStaff():
    fullName = request.form.get('staffFullName')
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

    staffShift = request.form.get("staffShift")
    staffCurrentState = request.form.get("staffCurrentState")

    staffImage = request.files["staffImage"]
    path = upload(staffImage)


    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    ID = fullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)

    db.execute("INSERT INTO Person(ID, Name, Gender, Contact, Address, Email) VALUES (:ID, :Name, :Gender, :Contact, :Address, :Email)",
                {"ID":ID, "Name":fullName, "Gender":gender, "Contact":phoneNumber, "Address":address, "Email":emailAddress})
    personID = (list(db.execute("SELECT Person.idPerson FROM Person WHERE Person.ID=:ID", {"ID":ID})))[0][0]
    db.execute("INSERT INTO Staff (Person_idPerson, Salary, Category, joiningDate, Qualification, CurrentState, Shift, Campus, DOB) VALUES (:ID, :Salary, :Category, :joiningDate, :Qualification, :CurrentState, :Shift, :Campus, :DOB)",{"ID":personID, "Salary":salary, "Category":staffCategory, "joiningDate":joiningDate, "Qualification":qualification, "CurrentState":staffCurrentState, "Shift":staffShift, "Campus":campus, "DOB":dob})
    db.execute("INSERT INTO image (Person_idPerson, Path) VALUES (:Person_idPerson, :Path)",{"Person_idPerson":personID, "Path":path})

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
    donorCurrentState = request.form.get("donorCurrentState")
    donorDateDonationStarted = request.form.get("donorDateDonationStarted")
    donorOrganization = request.form.get("donorOrganization")
    donorRemarks = request.form.get("donorRemarks")

    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    print(donorFullName, personCount)
    ID = donorFullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)

    db.execute("INSERT INTO Person(ID, Name, Gender, Contact, Address, Email) VALUES (:ID, :Name, :Gender, :Contact, :Address, :Email)",
                {"ID":ID, "Name":donorFullName, "Gender":donorGender, "Contact":donorPhoneNumber, "Address":donorAddress, "Email":donorEmail})
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
    sponsorCurrentState = request.form.get("sponsorCurrentState")
    sponsorDateSponsorshipDue = request.form.get("sponsorDateSponsorshipDue")
    sponsorDateSponsorshipStart = request.form.get("sponsorDateSponsorshipStart")
    sponsorRemarks = request.form.get("sponsorRemarks")
    sponsorDesignation = request.form.get("sponsorDesignation")
    sponsorCompany = request.form.get("sponsorCompany")

    personCount = (list(db.execute("SELECT count(*) FROM Person")))[0][0] + 1
    print(sponsorFullName, personCount)
    ID = sponsorFullName[0] + ((5-len(str(personCount)))*"0") +str(personCount)

    db.execute("INSERT INTO Person(ID, Name, Gender, Contact, Address, Email) VALUES (:ID, :Name, :Gender, :Contact, :Address, :Email)",
                {"ID":ID, "Name":sponsorFullName, "Gender":sponsorGender, "Contact":sponsorPhoneNumber, "Address":sponsorAddress, "Email":sponsorEmail})
    personID = (list(db.execute("SELECT Person.idPerson FROM Person WHERE Person.ID=:ID", {"ID":ID})))[0][0]
    db.execute("INSERT INTO Sponsor(Person_idPerson, CurrentState, DateSponsorshipDue, Remarks, DateSponsorshipStarted, Company, Designation) VALUES (:ID, :CurrentState, :sponsorDateSponsorshipDue, :sponsorRemarks, :sponsorDateSponsorshipStart, :Company, :Designation)", {"ID":personID, "CurrentState":sponsorCurrentState, "sponsorDateSponsorshipDue":sponsorDateSponsorshipDue, "sponsorRemarks":sponsorRemarks, "sponsorDateSponsorshipStart":sponsorDateSponsorshipStart, "Company":sponsorCompany, "Designation":sponsorDesignation})

    db.commit()

    return redirect(url_for("registerSponsorLink"))

#endregion


#region edit registeration module
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

#endregion


#region view profile module
@app.route("/viewProfilesPage")
def viewProfilesPage():
    mode = {'Student': False, 'Staff': False, 'Sponsor': False, 'Donor': False}
    return render_template("viewProfiles.html", mode=mode, data={})

# @app.route("/viewProfiles")
# def viewProfiles():
#     data = []
#     mode = {"Student": False, "Staff": False, "Sponsor": False, "Donor": False}
#     return render_template("viewProfiles.html", data=data, mode=mode)

@app.route("/viewProfileSearchFunction", methods=['POST'])
def viewProfileSearchFunction():
    data = []
    mode = {"Student": False, "Staff": False, "Sponsor": False, "Donor": False}
    category = request.form.get('viewProfileSearchCategory')
    if category == "1":
        mode['Student']=True
        data = db.execute("SELECT * FROM person, student, image, class WHERE person.idPerson = student.Person_idPerson AND student.Class_idClass = class.idClass AND image.Person_idPerson = person.idPerson")
    elif category == "2":
        mode["Staff"]=True
        data = db.execute("SELECT * FROM person, staff, image WHERE person.idPerson = staff.Person_idPerson AND image.Person_idPerson = person.idPerson")
    elif category == "3":
        mode["Sponsor"]=True
        data = db.execute("SELECT * FROM person, sponsor WHERE person.idPerson = sponsor.Person_idPerson")
    else:
        mode["Donor"]=True
        data = db.execute("SELECT * FROM person, donor WHERE person.idPerson = donor.Person_idPerson")

    # print(category)
    # data = list(db.execute("SELECT * FROM Person,Staff "))
    # print(data)
    return render_template("viewProfiles.html", data=data, mode=mode)

#endregion


#region finance module
@app.route("/viewFinance")
def viewFinance():
    return render_template("finance.html")


@app.route("/viewFinanceEntry")
def viewFinanceEntry():
    return render_template("financeEntry.html")


@app.route("/viewFinanceItem")
def viewFinanceItem():
    return render_template("financeItem.html")

#endregion


#region attendance module
@app.route("/viewAttendance")
def viewAttendance():
    classes = db.execute("SELECT Class.Name FROM Class")
    return render_template("Attendance.html", classes=classes,attendances=[],days=[])



@app.route("/searchViewAttendance", methods=["POST"])
def searchViewAttendance():
    attendees = request.form.get('selectAttendeesVA')
    Class = request.form.get("viewAttendanceSelectClass")
    attendanceDate = request.form.get('dateVA')
    print(attendees,Class, attendanceDate)
    classes = db.execute("SELECT Class.Name FROM Class")                # for populating the select box class again

    attendances = []
    month = list(db.execute("SELECT MONTH(:attendanceDate)",{'attendanceDate':attendanceDate}))[0][0]
    year = list(db.execute("SELECT YEAR(:attendanceDate)",{'attendanceDate':attendanceDate}))[0][0]

    classID = list(db.execute("SELECT class.idClass from class WHERE class.Name =:Class", {"Class":Class}))[0][0]
    # for students
    if attendees == "Student":
        dataOfAttendees = list(db.execute("SELECT person.idPerson, person.ID, person.Name FROM person, student WHERE person.idPerson = student.Person_idPerson AND student.Class_idClass = :classID", {"classID":classID}))
    # for staff
    else:
        dataOfAttendees = list(db.execute("SELECT person.idPerson, person.ID, person.Name FROM person, staff WHERE person.idPerson = staff.Person_idPerson"))

    numberOfDays = 0
    days = []
    for i in range(1,31+1):
        try:
            dt = datetime.datetime(year, month, i).strftime("%a")
        except:
            continue
        else:
            numberOfDays += 1
            days.append((i,dt))

    for person in dataOfAttendees:
        # attendance = list(db.execute(f"SELECT * FROM attendance WHERE attendance.Person_idPerson = {person[0]} AND MONTH(attendance.Date) = {month} AND YEAR(attendance.Date)= {year}"))
        attendanceOfOnePerson = []
        totalAttendances = 0
        totalPresences = 0
        totalLates = 0
        totalLeaves = 0
        totalAbsences = 0
        for i in range(1,numberOfDays+1):
            date = str(year) + '-' + str(month).zfill(2) + '-' + str(i).zfill(2)
            attendance = list(db.execute("SELECT attendance.State FROM attendance WHERE attendance.Person_idPerson = :idPerson AND attendance.Date = :attendanceDate", {'attendanceDate':date, 'idPerson':person[0]}))
            if len(attendance) == 0:
                attendanceOfOnePerson.append('')
            else:
                if attendance[0][0] == 1:
                    attendanceOfOnePerson.append('P')
                    totalAttendances += 1
                    totalPresences += 1
                if attendance[0][0] == 2:
                    attendanceOfOnePerson.append('L')
                    totalAttendances += 1
                    totalLates += 1
                if attendance[0][0] == 3:
                    attendanceOfOnePerson.append('LE')
                    totalAttendances += 1
                    totalLeaves += 1
                if attendance[0][0] == 4:
                    attendanceOfOnePerson.append('A')
                    totalAttendances += 1
                    totalAbsences += 1
        attendances.append((person[1], person[2], attendanceOfOnePerson, totalAttendances, totalPresences, totalLates, totalLeaves, totalAbsences))
    print(attendances)

    return render_template("Attendance.html", classes=classes,attendances=attendances,days=days)

@app.route("/viewMarkAttendance")
def viewMarkAttendance():
    classes = db.execute("SELECT Class.Name FROM Class")
    return render_template("MarkAttendance.html", classes=classes, people=[])


attendancePeople = []
attendanceDate = ''

@app.route("/searchMarkAttendance", methods=["POST"])
def searchMarkAttendance():
    global attendancePeople
    global attendanceDate
    attendees = request.form.get('selectAttendeesMA')
    Class = request.form.get("studentClassMA")
    attendanceDate = request.form.get('dateMA')
    print(attendees,Class, attendanceDate)
    classes = db.execute("SELECT Class.Name FROM Class")                # for populating the select box class again
    people = []
    # below is working for populating the marking attendance table
    if attendees != "Staff":
        classID = list(db.execute("SELECT class.idClass from class WHERE class.Name =:Class", {"Class":Class}))[0][0]
        people = list(db.execute("SELECT person.ID,person.Name FROM person,student WHERE person.idPerson=student.Person_idPerson AND student.Class_idClass=:classID",{"classID":classID}))
        attendancePeople = people
        # print(people)
    elif attendees == "Staff":
        people = list(db.execute("SELECT person.ID,person.Name FROM person,staff WHERE person.idPerson=staff.Person_idPerson"))
        attendancePeople = people
    return render_template("MarkAttendance.html", classes=classes, people=people)

@app.route("/submitAttendance",methods=["POST"])
def submitAttendance():
    global attendancePeople
    global attendanceDate
    state = {}
    for person in attendancePeople:
        state[person[0]] = request.form.get(person[0])
    print(state)
    for ID in state:
        personID = list(db.execute("SELECT person.idPerson FROM person WHERE person.ID=:ID",{"ID":ID}))[0][0]
        db.execute("INSERT INTO attendance (idAttendance, Person_idPerson, Date, State, Remarks) VALUES (NULL, :personID, :attendanceDate, :status, NULL);",{"personID":personID, "attendanceDate":attendanceDate, "status":state[ID]})
        db.commit()
    print("submitted attendance")
    attendancePeople = []
    attendanceDate = ""
    return redirect(url_for('viewMarkAttendance'))
#endregion


#region maintenance module
@app.route("/MaintenanceEntryLink")
def MaintenanceEntryLink():
    return render_template("MaintenanceEntry.html")

@app.route("/MaintenanceCategoryLink")
def MaintenanceCategoryLink():
    return render_template("MaintenanceCategory.html")


@app.route("/MaintenanceViewLink")
def MaintenanceViewLink():
    return render_template("MaintenanceActivity.html")

#endregion


#region test module
@app.route("/viewTestPage")
def viewTestPage():
    return render_template("Test.html")

#endregion


#region class module
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

#endregion


if __name__ == "__main__":
    app.run(debug=True)
