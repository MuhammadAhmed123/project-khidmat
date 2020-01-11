CREATE TABLE Module (
  idModule INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Name VARCHAR(255)  NULL  ,
  StartDate DATE  NULL  ,
  EndDate DATE  NULL    ,
PRIMARY KEY(idModule));



CREATE TABLE Item (
  idItem INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Name VARCHAR(255)  NULL  ,
  Description TEXT  NULL    ,
PRIMARY KEY(idItem));



CREATE TABLE Event (
  idEvent INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Name VARCHAR(255)  NULL  ,
  Date DATE  NULL  ,
  Budget INTEGER UNSIGNED  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idEvent));



CREATE TABLE Person (
  idPerson INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  ID VARCHAR(255)  NULL  ,
  Name VARCHAR(255)  NOT NULL  ,
  Gender VARCHAR(20)  NULL  ,
  Contact VARCHAR(20)  NOT NULL  ,
  Address TEXT  NULL  ,
  Email VARCHAR(255)  NULL    ,
PRIMARY KEY(idPerson));



CREATE TABLE VehicleMaintenanceCategory (
  idVehicleMaintenanceCategory INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Name VARCHAR(255)  NULL  ,
  Description TEXT  NULL    ,
PRIMARY KEY(idVehicleMaintenanceCategory));



CREATE TABLE Vehicle (
  idVehicle INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Name VARCHAR(255)  NULL  ,
  RegistrationNumber VARCHAR(255)  NULL    ,
PRIMARY KEY(idVehicle));



CREATE TABLE UtilityBills (
  idUtilityBills INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Category VARCHAR(255)  NULL  ,
  DueDate DATE  NULL  ,
  PaymentDate DATE  NULL  ,
  Amount INTEGER UNSIGNED  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idUtilityBills));



CREATE TABLE BloodHealth (
  idBloodHealth INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  BloodGroup VARCHAR(20)  NULL  ,
  HaemoglobinLevel FLOAT  NULL  ,
  Remarks TEXT  NULL  ,
  LastTestDate DATE  NULL    ,
PRIMARY KEY(idBloodHealth));



CREATE TABLE Class (
  idClass INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Name VARCHAR(20)  NULL  ,
  Campus VARCHAR(255)  NULL    ,
PRIMARY KEY(idClass));



CREATE TABLE Staff (
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  Salary INTEGER UNSIGNED  NOT NULL  ,
  Category VARCHAR(255)  NULL  ,
  JoiningDate DATE  NULL  ,
  Qualification TEXT  NULL  ,
  CurrentState VARCHAR(255)  NULL  ,
  Shift VARCHAR(255)  NULL  ,
  Campus VARCHAR(255)  NULL  ,
  DOB DATE  NULL    ,
PRIMARY KEY(Person_idPerson)  ,
INDEX Staff_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Sponsor (
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  CurrentState VARCHAR(255)  NULL  ,
  DateSponsorshipDue DATE  NULL  ,
  Remarks TEXT  NULL  ,
  DateSponsorshipStarted DATE  NULL  ,
  Company VARCHAR(255)  NULL  ,
  Designation VARCHAR(255)  NULL    ,
PRIMARY KEY(Person_idPerson)  ,
INDEX Sponsor_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Attendance (
  idAttendance INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  Date DATE  NULL  ,
  State INTEGER UNSIGNED  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idAttendance)  ,
INDEX Attendance_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE VehicleRegistration (
  idVehicleRegistration INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Vehicle_idVehicle INTEGER UNSIGNED  NOT NULL  ,
  Date DATE  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idVehicleRegistration)  ,
INDEX VehicleRegistration_FKIndex1(Vehicle_idVehicle),
  FOREIGN KEY(Vehicle_idVehicle)
    REFERENCES Vehicle(idVehicle)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE BuyingActivity (
  idBuyingActivity INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Item_idItem INTEGER UNSIGNED  NOT NULL  ,
  BuyingDate DATE  NULL  ,
  Quantity INTEGER UNSIGNED  NULL  ,
  BuyingPrice INTEGER UNSIGNED  NULL    ,
PRIMARY KEY(idBuyingActivity)  ,
INDEX BuyingActivity_FKIndex1(Item_idItem),
  FOREIGN KEY(Item_idItem)
    REFERENCES Item(idItem)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Increments (
  idIncrements INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Staff_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  Percentage INTEGER UNSIGNED  NULL  ,
  Remarks TEXT  NULL  ,
  DateIssued DATE  NULL  ,
  IsFirstIncrement BIT  NULL    ,
PRIMARY KEY(idIncrements)  ,
INDEX Increments_FKIndex1(Staff_Person_idPerson),
  FOREIGN KEY(Staff_Person_idPerson)
    REFERENCES Staff(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Image (
  idImage INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  Path VARCHAR(255)  NULL    ,
PRIMARY KEY(idImage)  ,
INDEX Image_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Deductions (
  idDeductions INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Staff_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  DeductedLeaves INTEGER UNSIGNED  NULL  ,
  AmountDeducted INTEGER UNSIGNED  NULL  ,
  DateOfDeduction DATE  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idDeductions)  ,
INDEX Deductions_FKIndex1(Staff_Person_idPerson),
  FOREIGN KEY(Staff_Person_idPerson)
    REFERENCES Staff(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Donor (
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  DateDonoationStarted DATE  NULL  ,
  CurrentState VARCHAR(255)  NULL  ,
  Organization VARCHAR(255)  NULL    ,
PRIMARY KEY(Person_idPerson)  ,
INDEX Donor_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Donation (
  idDonation INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  DateDonated DATE  NULL  ,
  Quantity INTEGER UNSIGNED  NULL  ,
  Remarks TEXT  NULL  ,
  Category VARCHAR(255)  NULL    ,
PRIMARY KEY(idDonation)  ,
INDEX Donation_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE VehicleMaintenance (
  idVehicleMaintenance INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  VehicleMaintenanceCategory_idVehicleMaintenanceCategory INTEGER UNSIGNED  NOT NULL  ,
  Vehicle_idVehicle INTEGER UNSIGNED  NOT NULL  ,
  Expense INTEGER UNSIGNED  NULL  ,
  Date DATE  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idVehicleMaintenance)  ,
INDEX VehicleMaintenance_FKIndex1(Vehicle_idVehicle)  ,
INDEX VehicleMaintenance_FKIndex2(VehicleMaintenanceCategory_idVehicleMaintenanceCategory),
  FOREIGN KEY(Vehicle_idVehicle)
    REFERENCES Vehicle(idVehicle)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(VehicleMaintenanceCategory_idVehicleMaintenanceCategory)
    REFERENCES VehicleMaintenanceCategory(idVehicleMaintenanceCategory)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Test (
  idTest INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Module_idModule INTEGER UNSIGNED  NOT NULL  ,
  Class_idClass INTEGER UNSIGNED  NOT NULL  ,
  Marks INTEGER UNSIGNED  NULL  ,
  TestDate DATE  NULL  ,
  isMid BIT  NULL  ,
  isFinal BIT  NULL  ,
  Name VARCHAR(45)  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idTest)  ,
INDEX Test_FKIndex1(Class_idClass)  ,
INDEX Test_FKIndex2(Module_idModule),
  FOREIGN KEY(Class_idClass)
    REFERENCES Class(idClass)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(Module_idModule)
    REFERENCES Module(idModule)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Student (
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  BloodHealth_idBloodHealth INTEGER UNSIGNED  NOT NULL  ,
  Sponsor_Person_idPerson INTEGER UNSIGNED  NULL  ,
  Class_idClass INTEGER UNSIGNED  NOT NULL  ,
  Religion VARCHAR(255)  NULL  ,
  LastAttendedSchool VARCHAR(255)  NULL  ,
  LastAttendedSchoolFee VARCHAR(255)  NULL  ,
  Shift VARCHAR(255)  NULL  ,
  TestDate DATE  NULL  ,
  InterviewDate DATE  NULL  ,
  FathersOcuupation VARCHAR(255)  NULL  ,
  FathersEarning INTEGER UNSIGNED  NULL  ,
  MothersOccupation VARCHAR(255)  NULL  ,
  MothersEarning INTEGER UNSIGNED  NULL  ,
  UniformMeasurement TEXT  NULL  ,
  UniformFees INTEGER UNSIGNED  NULL  ,
  NoOfSiblings INTEGER UNSIGNED  NULL  ,
  CurrentState VARCHAR(255)  NULL  ,
  DOB DATE  NULL  ,
  Campus VARCHAR(255)  NULL  ,
  GuardianName VARCHAR(255)  NULL  ,
  TransferLeavingCertificate BIT  NULL  ,
  SponsorLetter BIT  NULL  ,
  SchoolRules BIT  NULL  ,
  HealthFees INTEGER UNSIGNED  NULL  ,
  SchoolFees INTEGER UNSIGNED  NULL    ,
PRIMARY KEY(Person_idPerson)  ,
INDEX Student_FKIndex1(Person_idPerson)  ,
INDEX Student_FKIndex2(Class_idClass)  ,
INDEX Student_FKIndex3(Sponsor_Person_idPerson)  ,
INDEX Student_FKIndex4(BloodHealth_idBloodHealth),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(Class_idClass)
    REFERENCES Class(idClass)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(Sponsor_Person_idPerson)
    REFERENCES Sponsor(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(BloodHealth_idBloodHealth)
    REFERENCES BloodHealth(idBloodHealth)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE StudentFeesPayment (
  idStudentFeesPayment INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Student_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  Category VARCHAR(255)  NULL  ,
  Amount INTEGER UNSIGNED  NULL  ,
  Date DATE  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idStudentFeesPayment)  ,
INDEX StudentFeesPayment_FKIndex1(Student_Person_idPerson),
  FOREIGN KEY(Student_Person_idPerson)
    REFERENCES Student(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE TyphoidRecord (
  idTyphoidRecord INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Student_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  DateOfTest DATE  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idTyphoidRecord)  ,
INDEX TyphoidRecord_FKIndex1(Student_Person_idPerson),
  FOREIGN KEY(Student_Person_idPerson)
    REFERENCES Student(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE GeneralENT (
  idGeneralENT INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Student_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  DateOfTest DATE  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idGeneralENT)  ,
INDEX GeneralENT_FKIndex1(Student_Person_idPerson),
  FOREIGN KEY(Student_Person_idPerson)
    REFERENCES Student(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE HepatitisRecord (
  Student_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  HaveHapatitisDose BIT  NULL  ,
  HepatitisDose1 DATE  NULL  ,
  HepatitisDose2 DATE  NULL  ,
  HepatitisDose3 DATE  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(Student_Person_idPerson)  ,
INDEX HepatitisRecord_FKIndex1(Student_Person_idPerson),
  FOREIGN KEY(Student_Person_idPerson)
    REFERENCES Student(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE EyeCheckup (
  idEyeCheckup INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Student_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  DateOfTest DATE  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idEyeCheckup)  ,
INDEX EyeCheckup_FKIndex1(Student_Person_idPerson),
  FOREIGN KEY(Student_Person_idPerson)
    REFERENCES Student(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE SiblingsAtTGS (
  Student_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  Person_idPerson INTEGER UNSIGNED  NOT NULL    ,
PRIMARY KEY(Student_Person_idPerson, Person_idPerson)  ,
INDEX Student_has_Person_FKIndex1(Student_Person_idPerson)  ,
INDEX Student_has_Person_FKIndex2(Person_idPerson),
  FOREIGN KEY(Student_Person_idPerson)
    REFERENCES Student(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Student_has_Test (
  Student_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  Test_idTest INTEGER UNSIGNED  NOT NULL  ,
  ObtainedMarks INTEGER UNSIGNED  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(Student_Person_idPerson, Test_idTest)  ,
INDEX Student_has_Test_FKIndex1(Student_Person_idPerson)  ,
INDEX Student_has_Test_FKIndex2(Test_idTest),
  FOREIGN KEY(Student_Person_idPerson)
    REFERENCES Student(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(Test_idTest)
    REFERENCES Test(idTest)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);
