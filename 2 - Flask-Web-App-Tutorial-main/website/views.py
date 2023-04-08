from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from .models import Note, Ratings, StudentsInfo, Result, Class
from . import db
import json

views = Blueprint('views', __name__)

#app.secret_key = 'mysecretkey'

@views.route('/', methods=['GET', 'POST'])
def home():
    session['status'] = 'out'
    session['position'] = ''
    if request.method == 'POST': 
        note = request.form.get('note')
        rate = request.form.get('rate')

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=1, rate=rate)  #providing the schema for the note 
            db.session.add(new_note) 
            db.session.commit()
            flash('Note added!', category='success')

    rating = Ratings.query.all()
    return render_template("home.html",ratings=rating)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == 1:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/addSubs', methods=['GET', 'POST'])
def addSubs():
    session['status'] = 'pending'
    session['position'] = 'student'
    stuInfos = StudentsInfo.query.filter_by(student_id=session['userId'])
    
    if request.method == 'POST': 
        for i in range(0, session['numCourse']):
            x=str(i)
            name = request.form.get('name'+x) 
            course = request.form.get('course'+x)
            status = request.form.get('status'+x)

            if len(course) < 1:
                flash('Note is too short!', category='error') 
            else:
                addCourse = StudentsInfo(professorName=name, enrolledCourse=course, evalutationStatus=status, student_id=session['userId'])  #providing the schema for the note 
                db.session.add(addCourse) 
                db.session.commit()            
                
                flash('Note added!', category='success')

        session['status'] = 'in'
        #session['userId'] = session['student']
        return redirect(url_for('views.chooseProf'))

    return render_template("addSubs.html",userNow=stuInfos)


@views.route('/chooseProf', methods=['GET', 'POST'])
def chooseProf():
    stuInfos = StudentsInfo.query.filter_by(student_id=session['userId'])

    #session.pop('currentFacultyName', None)
    #session.pop('course', None)

    if request.method == 'POST': 
        facultyName = request.form.get('facultyNames')
        course = request.form.get('course')
        evalStatus = request.form.get('evalStatus')
        session['currentFacultyName'] = facultyName
        session['currentCourse'] = course
        session['evalStatus'] = evalStatus
        return redirect(url_for('views.form'))

    return render_template("chooseProf.html", stuInfo=stuInfos)


@views.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        rate1 = request.form.get('ARate1')
        rate2 = request.form.get('ARate2')
        rate3 = request.form.get('ARate3')
        rate4 = request.form.get('ARate4')
        rate5 = request.form.get('ARate5')

        rate1 = int(rate1)
        rate2 = int(rate2)
        rate3 = int(rate3)
        rate4 = int(rate4)
        rate5 = int(rate5)

        rateA = (rate1+rate2+rate3+rate4+rate5)/5

        result = Result.query.filter_by(facultyName=session['currentFacultyName'],course=session['currentCourse'], facultyClass=session['userClass']).first()#,facultyClass

        myClass = Class.query.filter_by(className=session['userClass']).first() 
        classNow = myClass.classNumOfStudent
        classNow = str(classNow)
        
        if result:
            resultExist = Result.query.filter_by(facultyName=session['currentFacultyName'],course=session['currentCourse']).first()

            # Update the attribute(s) of the record(s) you want to modify
            resultExist.catA = (resultExist.catA + rateA) / 2
            db.session.commit()

            x=resultExist.studentsAnswered.split()
            y=x[0]
            y=int(y)
            z=y+1
            z=str(z)
            i= z+" / "+classNow
            
            resultExist.studentsAnswered = i
            db.session.commit()

            evalStat = StudentsInfo.query.filter_by(professorName=session['currentFacultyName'], enrolledCourse=session['currentCourse'],student_id=session['userId']).first()            
            evalStat.evalutationStatus = "YES"
            db.session.commit()

            flash('Account created!', category='success')
            return redirect(url_for('views.chooseProf'))
        else:
            saveAnsweredStudents = "0 / " + classNow

            new_result = Result(catA=rateA, facultyName=session['currentFacultyName'], course=session['currentCourse'], campus="LIPA", college=session['userCollege'], facultyClass=session['userClass'], studentsAnswered=saveAnsweredStudents, )#, user_id=current_user.id
            db.session.add(new_result)
            db.session.commit()

            evalStat = StudentsInfo.query.filter_by(professorName=session['currentFacultyName'], enrolledCourse=session['currentCourse'],student_id=session['userId']).first()            
            evalStat.evalutationStatus = "YES"
            db.session.commit()

            flash('Account created!', category='success')
            return redirect(url_for('views.chooseProf'))

    return render_template("form.html")

@views.route('/showRec')
def showRec():
    session['username'] = 'password'
    rating = Ratings.query.all()

    return render_template("showRec.html",ratings=rating)



@views.route('/predictMe')
def predictMe():
    usName = session['username'] 

    import pandas as pd

    import matplotlib.pyplot as plt
    import seaborn as sns

    import numpy as np
    from sklearn.model_selection import train_test_split, GridSearchCV
    from sklearn.linear_model import LinearRegression, LogisticRegression
    from sklearn.metrics import r2_score, accuracy_score, confusion_matrix
    from sklearn.tree import DecisionTreeClassifier
    from sklearn import svm, metrics
    import pickle

    pickle_model = pickle.load(open('logModel_pickle', 'rb'))
    
    if request.method == 'POST':
        rate1 = request.form.get('rateA')
        rate2 = request.form.get('rateB')

    import pickle
    import pandas as pd

    pickle_model = pickle.load(open('logModel_pickle', 'rb'))

    df = pd.DataFrame({'A': [1], 'B': [2], 'C': [3], 'D': [4], 'APS': [5]})
    df

    picklePred = pickle_model.predict(df)
    picklePred

    user = Ratings.query.filter_by(id=1).first()

    # Update the attribute(s) of the record(s) you want to modify
    user.rateA = 10

    # Commit the changes to the database
    db.session.commit()
    
    return render_template("predictMe.php", pred=picklePred, userName=usName)