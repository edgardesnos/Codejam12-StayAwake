import cv2
from face_detector import FaceDetector
from face_mesh import FaceMeshDetector
import geocoder
import requests
import time

class VideoCamera(object):
    def __init__(self):
        self.face_detector = FaceDetector()
        self.face_mesh_detector = FaceMeshDetector()

        # Find the first available working webcam
        camera_feed_val = 0
        while camera_feed_val < 5:
            self.video = cv2.VideoCapture(camera_feed_val)
            try:
                ret, frame = self.video.read()
                ret, jpeg = cv2.imencode(".jpg", frame)
                break
            except:
                camera_feed_val += 1
        if camera_feed_val >= 5:
            raise Exception("No functioning video camera.")
    
    def __del__(self):
        self.video.release()


    def get_latitude(self):
        # use geocoder to get coordinates based on this ip address
        g = geocoder.ip('me')
        coords = g.latlng
        return coords[0]

    def get_longitude(self):
        g = geocoder.ip('me')
        coords = g.latlng
        return coords[1]

    def report_drowsy(self):
        # send a POST request to the backend
        # parameters: latitude, longitude, time
        url = 'http://127.0.0.1:5001/incidents/report'
        latitude = self.get_latitude()
        longitude = self.get_longitude()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        print (latitude, longitude)
        headers = {'content-type': 'application/json'}
        body = '{"latitude":"' + str(latitude) + '" ,"longitude":"' + str(longitude) + '", "time": "' + str(now) + '"}'

        req = requests.post(url, headers=headers, data=body)

        print(req.status_code)
        print(req.headers)
        print(req.text)

    def get_frame(self):
        ret, frame = self.video.read()
        #frame = self.face_detector.detect_face(frame)
        frame = self.face_mesh_detector.detect_mesh(frame)
        # is drowsy?
            # play sound
            # get data
            # save to db
        # self.report_drowsy()
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()
        