-- Creating the database and setting the current database to use
CREATE DATABASE ITDrivingSchool;
USE ITDrivingSchool;

-- Creating a table to store instructor details
CREATE TABLE Instructors (
    InstructorID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(255)
);

-- Creating a table to store student details
CREATE TABLE Students (
    StudentID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    PhoneNumber VARCHAR(15),
    Email VARCHAR(255)
);

-- Creating a table to store details about driving lessons
CREATE TABLE Lessons (
    LessonID INT AUTO_INCREMENT PRIMARY KEY,
    InstructorID INT,
    StudentID INT,
    LessonType ENUM('Introductory', 'Standard', 'Pass Plus', 'Driving Test'),
    LessonDate DATETIME,
    DurationHours INT,
    FOREIGN KEY (InstructorID) REFERENCES Instructors(InstructorID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
);

-- Inserting additional data into the Instructors table
INSERT INTO Instructors (FirstName, LastName, PhoneNumber, Email) VALUES
('Alice', 'Johnson', '3456789012', 'alice.johnson@passit.com'),
('Bob', 'Lee', '4567890123', 'bob.lee@passit.com'),
('Carol', 'Taylor', '5678901234', 'carol.taylor@passit.com'),
('David', 'Brown', '6789012345', 'david.brown@passit.com'),
('Emma', 'Davis', '7890123456', 'emma.davis@passit.com'),
('Frank', 'Miller', '8901234567', 'frank.miller@passit.com'),
('Grace', 'Wilson', '9012345678', 'grace.wilson@passit.com'),
('Henry', 'Moore', '0123456789', 'henry.moore@passit.com'),
('Ivy', 'Taylor', '1234509876', 'ivy.taylor@passit.com'),
('Jack', 'Smith', '2345619870', 'jack.smith@passit.com'),
('Kathy', 'Lee', '3456721981', 'kathy.lee@passit.com'),
('Louis', 'Clark', '4567832192', 'louis.clark@passit.com'),
('Maria', 'Lewis', '5678943213', 'maria.lewis@passit.com'),
('Nathan', 'Walker', '6789054324', 'nathan.walker@passit.com'),
('Olivia', 'Allen', '7890165435', 'olivia.allen@passit.com'),
('Peter', 'Young', '8901276546', 'peter.young@passit.com'),
('Queen', 'Harris', '9012387657', 'queen.harris@passit.com'),
('Rachel', 'Nelson', '0123498768', 'rachel.nelson@passit.com'),
('Steve', 'Morris', '1234987650', 'steve.morris@passit.com'),
('Tina', 'Rivera', '2345908761', 'tina.rivera@passit.com');

-- Inserting additional data into the Students table
INSERT INTO Students (FirstName, LastName, PhoneNumber, Email) VALUES
('Charlie', 'Green', '7456789012', 'charlie.green@students.passit.com'),
('Daisy', 'Black', '6567890123', 'daisy.black@students.passit.com'),
('Ethan', 'King', '5678901234', 'ethan.king@students.passit.com'),
('Fiona', 'Knight', '4789012345', 'fiona.knight@students.passit.com'),
('George', 'Lee', '3890123456', 'george.lee@students.passit.com'),
('Hannah', 'Scott', '2901234567', 'hannah.scott@students.passit.com'),
('Irene', 'Carter', '1012345678', 'irene.carter@students.passit.com'),
('James', 'Phillips', '2123456789', 'james.phillips@students.passit.com'),
('Kara', 'Evans', '3234567890', 'kara.evans@students.passit.com'),
('Leo', 'Parker', '4345678901', 'leo.parker@students.passit.com'),
('Mia', 'Edwards', '5456789012', 'mia.edwards@students.passit.com'),
('Noah', 'Collins', '6567890123', 'noah.collins@students.passit.com'),
('Olga', 'Stewart', '7678901234', 'olga.stewart@students.passit.com'),
('Pablo', 'Sanchez', '8789012345', 'pablo.sanchez@students.passit.com'),
('Quinn', 'Morris', '9890123456', 'quinn.morris@students.passit.com'),
('Ruby', 'Cook', '0901234567', 'ruby.cook@students.passit.com'),
('Steven', 'Bailey', '2012345678', 'steven.bailey@students.passit.com'),
('Tara', 'Wilson', '3123456789', 'tara.wilson@students.passit.com'),
('Uma', 'Franklin', '4234567890', 'uma.franklin@students.passit.com'),
('Victor', 'Nguyen', '5345678901', 'victor.nguyen@students.passit.com');

-- Inserting additional data into the Lessons table
INSERT INTO Lessons (InstructorID, StudentID, LessonType, LessonDate, DurationHours) VALUES
(6, 16, 'Introductory', '2024-05-26 10:00:00', 2),
(7, 17, 'Standard', '2024-05-27 11:00:00', 1),
(8, 18, 'Pass Plus', '2024-05-28 09:00:00', 3),
(9, 19, 'Driving Test', '2024-05-29 14:00:00', 2),
(10, 20, 'Introductory', '2024-05-30 10:00:00', 1),
(6, 11, 'Standard', '2024-05-31 13:00:00', 2),
(7, 12, 'Pass Plus', '2024-06-01 08:00:00', 3),
(8, 13, 'Driving Test', '2024-06-02 15:00:00', 1),
(9, 14, 'Introductory', '2024-06-03 11:00:00', 2),
(10, 15, 'Standard', '2024-06-04 16:00:00', 1),
(6, 16, 'Pass Plus', '2024-06-05 09:30:00', 3),
(7, 17, 'Driving Test', '2024-06-06 13:00:00', 2),
(8, 18, 'Introductory', '2024-06-07 10:00:00', 1),
(9, 19, 'Standard', '2024-06-08 14:00:00', 2),
(10, 20, 'Pass Plus', '2024-06-09 08:00:00', 3);
