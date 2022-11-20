import cv2
from face_mesh import FaceMeshDetector
from drowsiness_alerter import DrowsinessAlerter

class VideoCamera(object):
    def __init__(self):
        self.face_mesh_detector = FaceMeshDetector()
        self.drowsiness_alerter = DrowsinessAlerter()

        # Find the first available working webcam
        camera_feed_val = 2
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

    def get_frame(self):
        ret, frame = self.video.read()
        #frame = self.face_detector.detect_face(frame)
        frame, is_drowsy = self.face_mesh_detector.detect_mesh(frame)
        self.drowsiness_alerter.should_alert(is_drowsy)
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()
        