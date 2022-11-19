import cv2

class FaceDetector:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier("./data/haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier("./data/haarcascade_eye.xml")

    def detect_face(self, image):
        # convert to gray scale of each frames
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detects faces of different sizes in the input image
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x,y,w,h) in faces:
            # To draw a rectangle in a face
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            
            # Detects eyes of different sizes in the input image
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            
            #To draw a rectangle in eyes
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2)

        return image