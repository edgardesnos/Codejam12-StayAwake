from flask import Flask
from flask import request
import pyodbc

app = Flask(__name__)

@app.route('/hello')
def hello():
    return "Hello."

@app.route('/incidents/report', methods = ['POST'])
def report_incident():
    json = request.json
    x = json['x']
    y = json['y']
    address = json['address'] # probably should look up the address using coordinates instead of passing it here
    time = json['time']

    # create a new incident report in the database
    insert_statement = "INSERT INTO Drowsiness_Report(gps_x_cord, gps_y_cord, time, incident_address) VALUES (" + x + ", " + y + ", '" +  time + "' , '" + address + "')"
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
        return "Successful Login!"
    else:
        return "Login failed."

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

if __name__ == '__main__':

    app.run(port="8080")
    # app.run()