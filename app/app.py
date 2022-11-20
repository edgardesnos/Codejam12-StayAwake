from flask import Flask, render_template, Response, request
from camera import VideoCamera
import pyodbc
import pandas as pd
#from webservices import app_webservices

app = Flask(__name__)

@app.route("/")
def index():
    # rendering webpage
    return render_template("p_index.html")

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")

@app.route("/video_feed")
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route('/hello')
def hello():
    return "Hello."

@app.route('/incidents/report', methods = ['POST'])
def report_incident():
    json = request.json
    latitude = json['latitude']
    longitude = json['longitude']
    time = json['time']

    # create a new incident report in the database
    print(latitude)
    print(longitude)
    print(time)
    print(str(latitude))
    insert_statement = "INSERT INTO Drowsiness_Report(latitude, longitude, time) VALUES (" + str(latitude) + ", " + str(longitude) + ", '" +  str(time) + "')"
    insert(insert_statement)
    return "Inserted into database" # TODO: error checking? this return value is not helpful


# @app.route('/login', methods = ['POST'])
@app.route('/login/<username>/<password>')
def confirm_login(username, password):

    # check if the username and password combination is valid in the db
    print("SELECT * from Users where uname = '" + username + "' AND pass = '" + password + "'")
    results = select_query("SELECT * from Users where uname = '" + username + "' AND pass = '" + password + "'")
    # if 1 row returned, then we logged in successfully
    count = len(results)
    if (count == 1): # username is unique in db, so not going to be more than 1
        return "success"
    else:
        return "fail"

def print_all_drowsy_records():
    querytxt = "SELECT * FROM Drowsiness_Report"
    # results = select_query(querytxt)
    # for row in results:
    #     print("Record id: ", row[3])
    #     print("Latitude: ", row[0])
    #     print("Longitude: ", row[1])
    #     print("Time: ", row[2])
    #     print("\n")
    data = getDataFrameAllDrowsinessRecords()
    print(data)


def select_query(query):
    server = 'codejam12-sql-server.database.windows.net'
    database = 'codejam'
    username = 'nick'
    password = 'FuozZy4DK'
    connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
    cursor = connection.cursor() # the actual object we use to query
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    # return all records
    return results

# TODO: return something
def insert(statement):
    server = 'codejam12-sql-server.database.windows.net'
    database = 'codejam'
    username = 'nick'
    password = 'FuozZy4DK'
    connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
    cursor = connection.cursor() # the actual object we use to query
    cursor.execute(statement)
    connection.commit()
    connection.close()

@app.route('/incidents/all')
def getDataFrameAllDrowsinessRecords():
    server = 'codejam12-sql-server.database.windows.net'
    database = 'codejam'
    username = 'nick'
    password = 'FuozZy4DK'
    connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
    querytxt = "SELECT * FROM Drowsiness_Report"
    data = pd.read_sql(querytxt, connection)
    return render_template('dataDisplay.html', tables=[data.to_html(classes='data')], titles=data.columns.values)

if __name__ == "__main__":
    # defining server ip address and port
    # print_all_drowsy_records()
    app.run(host="127.0.0.1",port="5001", debug=True)
