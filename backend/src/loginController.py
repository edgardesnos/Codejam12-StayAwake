from flask import Flask
import pyodbc

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'

@app.route("/poop")
def poop():
    return 'Poop.'


# @app.route('/login', methods = ['POST'])
@app.route('/login/<username>/<password>')
def confirm_login():
    username = request.args['username']
    password = request.args['password']

    # check if the username and password combination is valid in the db
    results = select_query("SELECT * from Users where username = '" + username + " AND password = '" + password + "'")
    print(results)

def select_query(query):
    server = 'codejam12-sql-server.database.windows.net'
    database = 'codejam'
    username = 'nick'
    password = 'FuozZy4DK'
    connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
    cursor = connection.cursor() # the actual object we use to query
    cursor.execute(query)
    # return all records
    return cursor.fetchall()

    
    connection.close()

if __name__ == '__main__':

    app.run()