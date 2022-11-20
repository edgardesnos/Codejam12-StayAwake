import cv2
from face_mesh import FaceMeshDetector
import geocoder
import requests
import time
from drowsiness_alerter import DrowsinessAlerter

class VideoCamera(object):
    def __init__(self):
        self.face_mesh_detector = FaceMeshDetector()
        self.drowsiness_alerter = DrowsinessAlerter()

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


    def get_latitude_longitude(self):
        # use geocoder to get coordinates based on this ip address
        g = geocoder.ip('me')
        coords = g.latlng
        if coords is None:
            coords = (0, 0)
        return coords[0], coords[1]

    def report_drowsy(self):
        # send a POST request to the backend
        # parameters: latitude, longitude, time
        url = 'http://127.0.0.1:5001/incidents/report'
        latitude, longitude = self.get_latitude_longitude()
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        headers = {'content-type': 'application/json'}
        body = '{"latitude":"' + str(latitude) + '" ,"longitude":"' + str(longitude) + '", "time": "' + str(now) + '"}'

        req = requests.post(url, headers=headers, data=body)

    def get_frame(self):
        ret, frame = self.video.read()
        frame, is_drowsy = self.face_mesh_detector.detect_mesh(frame)
        alert_sent = self.drowsiness_alerter.should_alert(is_drowsy)
        if alert_sent:
            self.report_drowsy()
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()


        