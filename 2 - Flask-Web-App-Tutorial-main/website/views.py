from flask import Blueprint, render_template, request, flash, jsonify, session, redirect, url_for
from .models import StudentsInfo, Result
from . import db
import json

views = Blueprint('views', __name__)

#app.secret_key = 'mysecretkey'

@views.route('/', methods=['GET', 'POST'])
def home():
    session['status'] = 'out'
    session['position'] = ''
    return render_template("home.html")

"""  """

@views.route('/addSubs', methods=['GET', 'POST'])
def addSubs():
    session['position'] = 'student'
    stuInfos = StudentsInfo.query.filter_by(student_id=session['userId'])
    
    if request.method == 'POST': 
        for i in range(0, session['numCourse']):
            x=str(i)
            name = request.form.get('name'+x) 
            course = request.form.get('course'+x)
            status = request.form.get('status'+x)
            
            section = request.form.get('section'+x) 
            college = request.form.get('college'+x)
            campus = request.form.get('campus'+x)

            addCourse = StudentsInfo(professorName=name, enrolledCourse=course, evaluationStatus=status, studentSection=section, studentCollege=college, studentCampus=campus, student_id=session['userId'])  #providing the schema for the note 
            db.session.add(addCourse) 
            db.session.commit() 
                    
            resultExists = Result.query.filter_by(facultyName=name, course=course, facultyClass=section, college=college, campus=campus).first()

            if resultExists:
                x=resultExists.studentsAnswered.split()

                y=x[0]

                z=x[2]
                z=int(z)
                z=z+1
                z=str(z)

                newAnswered= y+" / "+z                
                resultExists.studentsAnswered = newAnswered
                db.session.commit()
            else:
                addCourse = Result(facultyName=name, course=course, facultyClass=section, college=college, campus=campus, studentsAnswered="0 / 1")  #providing the schema for the note 
                db.session.add(addCourse) 
                db.session.commit()            
                
            flash('Note added!', category='success')

            ###

        session['status'] = 'in'
        #session['userId'] = session['student']
        #session['status'] = 'in'
        return redirect(url_for('views.chooseProf'))

    return render_template("addSubs.html",userNow=stuInfos)


@views.route('/chooseProf', methods=['GET', 'POST'])
def chooseProf():
    session['numCourse'] = 0
    stuInfos = StudentsInfo.query.filter_by(student_id=session['userId'])

    #session.pop('currentFacultyName', None)
    #session.pop('course', None)

    if request.method == 'POST': 
        facultyName = request.form.get('facultyNames')
        course = request.form.get('course')
        campus = request.form.get('campus')
        college = request.form.get('college')
        section = request.form.get('class')
        evalStatus = request.form.get('evalStatus')

        session['currentFacultyName'] = facultyName
        session['currentCourse'] = course
        session['currentCampus'] = campus
        session['currentCollege'] = college
        session['currentClass'] = section
        session['evalStatus'] = evalStatus
        return redirect(url_for('views.form'))

    return render_template("chooseProf.html", stuInfo=stuInfos)


@views.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        comment = request.form.get('comment')

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
        
        #sentimentValue, saveComment = SentenceAnalysis(comment)   

        sentimentValue = 3

        saveComment = "No Algo"

        resultExist = Result.query.filter_by(facultyName=session['currentFacultyName'],course=session['currentCourse'], facultyClass=session['currentClass'], campus=session['currentCampus'], college=session['currentCollege']).first()#,facultyClass
        
        if resultExist:
            x=resultExist.studentsAnswered.split()

            y=x[0]
            y=int(y)
            y=y+1
            y=str(y)

            z=x[2]

            newAnswered= y+" / "+z 

            if resultExist.catA == None:
                overAllResult = (rateA + sentimentValue) / 2

                if overAllResult == 3:
                    sentimentResult = "Neutral"
                elif overAllResult < 3:
                    sentimentResult = "Not Excellent"
                else:
                    sentimentResult = "Excellent"

                resultExist.catA = rateA
                db.session.commit()

                resultExist.senAnalysis = sentimentValue
                db.session.commit()

                resultExist.result = sentimentResult
                db.session.commit()

                resultExist.studentsAnswered = newAnswered
                db.session.commit()
                
                if len(saveComment) > 3:
                    resultExist.comments = saveComment
                    db.session.commit()
                    
            else:
                # Update 
                resultExist.catA = (resultExist.catA + rateA) / 2
                db.session.commit()

                resultExist.senAnalysis = (resultExist.senAnalysis + sentimentValue) / 2   
                db.session.commit()

                overAllResult = (resultExist.catA + resultExist.senAnalysis) / 2

                if overAllResult == 3:
                    sentimentResult = "Neutral"
                elif overAllResult < 3:
                    sentimentResult = "Not Excellent"
                else:
                    sentimentResult = "Excellent"

                resultExist.result = sentimentResult
                db.session.commit()

                if len(saveComment) > 3:
                    if resultExist.comments == None:
                        resultExist.comments = saveComment
                        db.session.commit()
                    else:
                        resultExist.comments = resultExist.comments + " " + saveComment
                        db.session.commit()
                        
               
                resultExist.studentsAnswered = newAnswered
                db.session.commit()

            evalStat = StudentsInfo.query.filter_by(professorName=session['currentFacultyName'], enrolledCourse=session['currentCourse'],student_id=session['userId']).first()            
            evalStat.evaluationStatus = "YES"
            db.session.commit()

            flash('Account created!', category='success')
            return redirect(url_for('views.chooseProf'))

    return render_template("form.html")

@views.route('/showRec')
def showRec():
    records = Result.query.all()

    return render_template("showRec.html",records=records)

""" 

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

    #user = Ratings.query.filter_by(id=1).first()

    # Update the attribute(s) of the record(s) you want to modify
    #user.rateA = 10

    # Commit the changes to the database
    db.session.commit()
    
    return render_template("predictMe.php", pred=picklePred, userName=usName) """

"""
def SentenceAnalysis(userInput):
    import pandas as pd

    df = pd.read_csv('Comments-Dataset - Eng.csv')
    df = pd.DataFrame({'Comments': df['Comments'], 'Result':df['Result']})

    #Data cleaning and preprocessing
    import re
    import nltk
    nltk.download('stopwords')

    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    #Lemmatize
    corpus = []
    for i in range(0, len(df)):
        review = re.sub('[^a-zA-Z]', ' ', df['Comments'][i])
        review = review.lower()
        review = review.split()
        
        review = [lemmatizer.lemmatize(word) for word in review if not word in stopwords.words('english')]
        review = ' '.join(review)
        corpus.append(review)
        
    ## tokenize
    allWords=[]
    for i in corpus:
        words=nltk.word_tokenize(i)
        for word in words:
            allWords.append(word)

    #Creating the Bag of Words model
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(max_features=2500)
    X = cv.fit_transform(corpus).toarray()
    y=df['Result']

    # Train Test Split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 42)

    from sklearn.naive_bayes import MultinomialNB
    MNB_model = MultinomialNB().fit(X_train, y_train)

    #User Input
    userComment = userInput

    ### Dataset Preprocessing
    #from nltk.stem import WordNetLemmatizer
    #lemmatizer = WordNetLemmatizer()
    userCorpus = []

    userCommentLow = userComment
    userCommentLow = userCommentLow.lower()

    #Lemmatizing the user's input

    sentimentValue = 0
    if userCommentLow == "none" or userCommentLow == "none." or userCommentLow == "n/a" or userCommentLow == "n/a.":
        sentimentValue = 3
    else:
        review = re.sub('[^a-zA-Z]', ' ', userComment)
        review = review.lower()
        review = review.split()

        review = [lemmatizer.lemmatize(word) for word in review if not word in stopwords.words('english')]
        review = ' '.join(review)
        userCorpus.append(review)
        
    #tokenize user sentence
    userWords=[]
    for i in userCorpus:
        words=nltk.word_tokenize(i)
        for word in words:
            userWords.append(word)
            
    #check if user words exists in model
    duplicates = []
    seen = []

    for row in userWords:
        if row not in allWords:
            duplicates.append(row)
        else:
            seen.append(row)
            
    saveSenToDb = ""
    #predicting the result
    if sentimentValue == 0:
        if len(duplicates) < 1:
            corpus.append(userCorpus[0])

            X = cv.fit_transform(corpus).toarray()

            X = X[len(corpus)-1]

            newX = []
            newX.append(X)

            y_pred=MNB_model.predict(newX)

            corpus.append(userCorpus[0])

            X = cv.fit_transform(corpus).toarray()

            userX = X[len(corpus)-1]

            newX = []
            newX.append(userX)

            y_pred=MNB_model.predict(newX)
            predResult = y_pred[0]

            #assigning value
            if predResult == 1:
                sentimentValue = 5
            elif predResult == 0:
                sentimentValue = 1

            sentimentValue = int(sentimentValue)

            #cleaning dataframe
            dfSave = pd.DataFrame({'Comments': df['Comments'], 'Result':df['Result']})

            #saving the new comment to dataset
            dfSave.loc[len(dfSave)] = [userComment, predResult]

            dfSave.to_csv('Comments-Dataset - Eng.csv')

            saveSenToDb = userComment
        else:
            print("word doesn't exist")

    return sentimentValue, saveSenToDb"""
