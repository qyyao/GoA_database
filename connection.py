from flask import Flask, render_template, request,redirect,url_for
from flaskext.mysql import MySQL

app = Flask(__name__)
 app.config['MYSQL_DATABASE_HOST'] = 'localhost'
 app.config['MYSQL_DATABASE_USER'] = 'root'
 app.config['MYSQL_DATABASE_PASSWORD'] = ''
 app.config['MYSQL_DATABASE_DB'] = 'goa'



mysql = MySQL(app)




@app.route("/")
def homePage():
    return render_template("home.html")


@app.route('/events')
def events():
    cursor = mysql.get_db().cursor()
    string = "SELECT * FROM goaEvent ORDER BY Date;"
    cursor.execute(string)
    fetchdata = cursor.fetchall()
    string2 = "SELECT * FROM goaEvent A WHERE NOT EXISTS (SELECT Location FROM CanadianLocations B WHERE A.Location = B.Location);"
    cursor.execute(string2)
    fetchdata2 = cursor.fetchall()
    cursor.close()
    return render_template("events.html",events=fetchdata,eventsOC=fetchdata2)



@app.route('/suggestions',methods=['POST','GET'])
def suggestions():
    if request.method == 'POST':
        suggestion = request.form['SuggestionID']
        device = request.form['Device']
        text = request.form['Text']
        conn = mysql.get_db()
        cursor = mysql.get_db().cursor()
        cursor.execute("INSERT INTO AnonymousSuggestions (SuggestionID,Device,Text) VALUES (%s,%s,%s)",(suggestion,device,text))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('suggestions'))
    else:
        cursor = mysql.get_db().cursor()
        string = "SELECT * FROM AnonymousSuggestions;"
        cursor.execute(string)
        fetchdata = cursor.fetchall()
        cursor.close()
        return render_template("suggestions.html",suggestions=fetchdata)


@app.route('/eventDetails',methods=['GET','POST'])
def eventDetails():
    id = request.form['id']
    cursor = mysql.get_db().cursor()
    string = "SELECT * FROM goaEvent WHERE EventID = %s;"
    cursor.execute(string,(id))
    fetchdata = cursor.fetchall()
    cursor.close()
    return render_template("eventDetails.html",eventData=fetchdata)



@app.route('/suggestionDetails',methods=['GET','POST'])
def suggestionDetails():
    id = request.form['id']
    cursor = mysql.get_db().cursor()
    string = "SELECT * FROM AnonymousSuggestions WHERE SuggestionID = %s;"
    cursor.execute(string,(id))
    fetchdata = cursor.fetchall()
    cursor.close()
    return render_template("suggestionDetails.html",suggestionData=fetchdata)




@app.route('/lessons')
def lessons():
    cursor = mysql.get_db().cursor()
    string = "SELECT * FROM lesson ORDER BY weekNumber"
    cursor.execute(string)
    fetchdata = cursor.fetchall()
    cursor.close()
    return render_template("lessons.html", lessons = fetchdata)


@app.route('/lessonDetails/<string:ID>')
def lessonDetails(ID):
    cursor = mysql.get_db().cursor()
    string = "SELECT * FROM lesson WHERE LessonID = %s ;"
    cursor.execute(string, ID)
    lessonData = cursor.fetchall()
    cursor.close()
    return render_template("lessonDetails.html", lessonData = lessonData)


@app.route('/assignment/<string:lessonID>')
def assignment(lessonID):
    cursor = mysql.get_db().cursor()
    string = "SELECT * FROM assignment WHERE LessonID = %s ;"
    cursor.execute(string, lessonID)
    assignmentData = cursor.fetchall()
    cursor.close()
    return render_template("assignment.html", assignmentData = assignmentData)


@app.route('/challenge/<string:lessonID>')
def challenge(lessonID):
    cursor = mysql.get_db().cursor()
    string = "SELECT * FROM question WHERE ChallengeID IN (SELECT challengeID FROM challenge WHERE LessonID = %s);"
    cursor.execute(string, lessonID)
    questions = cursor.fetchall()
    cursor.close()
    return render_template("challenge.html", questions = questions)



@app.route('/students', methods=['GET', 'POST'])
def studentTable():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM goaUser")
    fetchdata = cursor.fetchall()
    cursor.close()
    #print(fetchdata)
    return render_template("students.html", student =fetchdata)


@app.route('/student_profile', methods=['GET', 'POST'])
def studentSearch():
    id = request.form['id']
    cursor = mysql.get_db().cursor()
    string = "SELECT * FROM goaUser WHERE UserID = %s ;"
    cursor.execute(string, id)
    fetchdata = cursor.fetchall()
    cursor.close()
    return render_template("student_profile.html", student=fetchdata)


@app.route('/teams',  methods=['GET', 'POST'])
def teams():
	cursor = mysql.get_db().cursor()
	string = "SELECT * FROM team ORDER BY VotesReceived DESC;"
	cursor.execute(string)
	fetchdata = cursor.fetchall()
	cursor.close()
	return render_template("teams.html", teams=fetchdata)

if __name__ == "__main__":
    app.run(debug=True)