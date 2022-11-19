import cv2
from face_detector import FaceDetector

class VideoCamera(object):
    def __init__(self):
       self.video = cv2.VideoCapture(2)
       self.face_detector = FaceDetector()
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        frame = self.face_detector.detect_face(frame)
        ret, jpeg = cv2.imencode(".jpg", frame)
        return jpeg.tobytes()