from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    rate = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    #rating = db.relationship('Ratings')

class Ratings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rateA = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    facultyName = db.Column(db.String(255))
    facultySrcode = db.Column(db.String(255))
    password = db.Column(db.String(255))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentName = db.Column(db.String(255))
    studentSrcode = db.Column(db.String(255))
    studentPassword = db.Column(db.String(255))
    studentSection = db.Column(db.String(255))
    studentCollege = db.Column(db.String(255))
    studentCampus = db.Column(db.String(255))
    numOfCourses = db.Column(db.Integer)
    notes = db.relationship('StudentsInfo')

class StudentsInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professorName = db.Column(db.String(255))
    enrolledCourse = db.Column(db.String(255))
    evalutationStatus = db.Column(db.String(255))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))




"""""

CREATE TABLE `classtbl` (
  `id` int(11) NOT NULL,
  `className` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `classNumOfStudent` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;



--

CREATE TABLE `facultyinfotbl` (
  `id` int(11) NOT NULL,
  `facultyName` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `course` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `section` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `campus` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `numOfStudents` int(11) DEFAULT NULL,
  `studentsAnswered` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




CREATE TABLE `perfomance_evaluation` (
  `id` int(11) NOT NULL,
  `facultyName` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `campus` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `college` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `course` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `class` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `studentsAnswered` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `A` float NOT NULL,
  `B` float NOT NULL,
  `C` float NOT NULL,
  `D` float NOT NULL,
  `APS` float NOT NULL,
  `comments` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `result` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--



CREATE TABLE `studentsinfotbl` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `srcode` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `enrolledCourse` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `section` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `professor` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `campus` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `evaluated` enum('NO','YES') COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




CREATE TABLE `studenttbl` (
  `id` int(11) NOT NULL,
  `studentName` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `studentSrcode` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `studentPassword` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `studentClass` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `studentCollege` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `studentCampus` varchar(255) COLLATE utf8_unicode_ci DEFAULT 'LIPA',
  `numOfCourses` int(11) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- """