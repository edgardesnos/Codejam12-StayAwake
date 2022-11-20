from flask import Flask, render_template, Response
from camera import VideoCamera
import jyserver.Flask as jsf
import requests, json, geocoder
app = Flask(__name__)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@app.route("/") # base URL (home page, first time being run)
def index():
    g = geocoder.ip('me')
    coords = g.latlng
    lat = coords[0]
    long = coords[1]
    url = f"https://dev.virtualearth.net/REST/v1/LocationRecog/{lat},{long}?&top=1&includeEntityTypes=address&key=As121dM81pVFCIUxLtVB3xYQ-ps7x7jCP7PlEFfvI4RM87V4OUkHV4h3lEpDGeUW"
    response = requests.get(url)
    data = response.json() 
    addr = data["resourceSets"][0]["resources"][0]["addressOfLocation"][0]["formattedAddress"]
    return render_template("index.html", address=addr)

@app.route("/login") # base URL (home page, first time being run)
def login(): 
    return render_template("login.html")
# def get_address(): 
#     #coordinates = App.get_coords()
#     #url = f"https://dev.virtualearth.net/REST/v1/LocationRecog/{coordinates[0]},{coordinates[1]}?&top=1&includeEntityTypes=address&key=As121dM81pVFCIUxLtVB3xYQ-ps7x7jCP7PlEFfvI4RM87V4OUkHV4h3lEpDGeUW"



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

if __name__ == "__main__":
    # defining server ip address and port
    app.run(host="0.0.0.0",port="5000", debug=True)