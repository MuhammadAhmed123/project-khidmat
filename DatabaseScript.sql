CREATE TABLE Person (
  idPerson INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  ID VARCHAR(255)  NULL  ,
  Name VARCHAR(255)  NOT NULL  ,
  GuardianName VARCHAR(255)  NULL  ,
  Gender VARCHAR(20)  NULL  ,
  Contact VARCHAR(20)  NOT NULL  ,
  Address TEXT  NULL  ,
  DOB DATE  NULL  ,
  Campus VARCHAR(255)  NULL  ,
  Email VARCHAR(255)  NULL    ,
PRIMARY KEY(idPerson));



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



CREATE TABLE Class (
  idClass INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Name VARCHAR(20)  NULL    ,
PRIMARY KEY(idClass));



CREATE TABLE Staff (
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  Salary INTEGER UNSIGNED  NOT NULL  ,
  Category VARCHAR(255)  NULL  ,
  JoiningDate DATE  NULL  ,
  Qualification TEXT  NULL    ,
PRIMARY KEY(Person_idPerson)  ,
INDEX Staff_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE MaintenanceCategory (
  idMaintenanceCategory INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Staff_Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  CategoryName VARCHAR(255)  NULL  ,
  DueTimeInterval VARCHAR(255)  NULL    ,
PRIMARY KEY(idMaintenanceCategory)  ,
INDEX MaintenanceCategory_FKIndex1(Staff_Person_idPerson),
  FOREIGN KEY(Staff_Person_idPerson)
    REFERENCES Staff(Person_idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE Sponsor (
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  CurrentState VARCHAR(255)  NULL  ,
  DateSponsorshipDue DATE  NULL  ,
  Remarks TEXT  NULL  ,
  DateSponsorshipStarted DATE  NULL    ,
PRIMARY KEY(Person_idPerson)  ,
INDEX Sponsor_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION);



CREATE TABLE MaintenanceActivity (
  idMaintenanceActivity INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  MaintenanceCategory_idMaintenanceCategory INTEGER UNSIGNED  NOT NULL  ,
  ExecutionDate DATE  NULL  ,
  Description TEXT  NULL    ,
PRIMARY KEY(idMaintenanceActivity)  ,
INDEX MaintenanceActivity_FKIndex1(MaintenanceCategory_idMaintenanceCategory),
  FOREIGN KEY(MaintenanceCategory_idMaintenanceCategory)
    REFERENCES MaintenanceCategory(idMaintenanceCategory)
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



CREATE TABLE Donation (
  idDonation INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Person_idPerson INTEGER UNSIGNED  NOT NULL  ,
  DateDonated DATE  NULL  ,
  Amount INTEGER UNSIGNED  NULL  ,
  Remarks TEXT  NULL    ,
PRIMARY KEY(idDonation)  ,
INDEX Donation_FKIndex1(Person_idPerson),
  FOREIGN KEY(Person_idPerson)
    REFERENCES Person(idPerson)
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



CREATE TABLE Test (
  idTest INTEGER UNSIGNED  NOT NULL   AUTO_INCREMENT,
  Module_idModule INTEGER UNSIGNED  NOT NULL  ,
  Class_idClass INTEGER UNSIGNED  NOT NULL  ,
  Marks INTEGER UNSIGNED  NULL  ,
  TestDate DATE  NULL  ,
  isMid BIT  NULL  ,
  isFinal BIT  NULL    ,
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
  NoOfSiblings INTEGER UNSIGNED  NULL    ,
PRIMARY KEY(Person_idPerson)  ,
INDEX Student_FKIndex1(Person_idPerson)  ,
INDEX Student_FKIndex2(Class_idClass)  ,
INDEX Student_FKIndex3(Sponsor_Person_idPerson),
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




