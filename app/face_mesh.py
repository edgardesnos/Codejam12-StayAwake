import mediapipe as mp
import cv2
from scipy.spatial import distance

class FaceMeshDetector:

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def EAR(self,eye):
        
        # horizontal
        C = distance.euclidean(eye[0], eye[1])
        # vertical
        A = distance.euclidean(eye[2], eye[3])
        B = distance.euclidean(eye[4], eye[5])
        # compute the eye aspect ratio
        ear = (A + B) / (2* C)
        # return the eye aspect ratio
        return ear

    def detect_mesh(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmark_coords = [(d.x, d.y, d.z) for d in face_landmarks.landmark]

                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_tesselation_style()
                )
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_contours_style()
                )
                # self.mp_drawing.draw_landmarks(
                #     image=image,
                #     landmark_list=face_landmarks,
                #     connections=self.mp_face_mesh.FACEMESH_IRISES,
                #     landmark_drawing_spec=None,
                #     connection_drawing_spec=self.mp_drawing_styles
                #     .get_default_face_mesh_iris_connections_style()
                # )
            y_size, x_size, _ = image.shape

            r_eye_coords = [[landmark_coords[33][0],landmark_coords[33][1]],[landmark_coords[133][0],landmark_coords[133][1]],
            [landmark_coords[160][0],landmark_coords[160][1]],[landmark_coords[144][0],landmark_coords[144][1]],
            [landmark_coords[158][0],landmark_coords[158][1]],[landmark_coords[153][0],landmark_coords[153][1]]] #width, height1, height2
            
            l_eye_coords = [[landmark_coords[362][0],landmark_coords[362][1]],[landmark_coords[263][0],landmark_coords[263][1]],
            [landmark_coords[385][0],landmark_coords[385][1]],[landmark_coords[380][0],landmark_coords[380][1]],
            [landmark_coords[387][0],landmark_coords[387][1]],[landmark_coords[373][0],landmark_coords[373][1]]]

            image = cv2.line(image, (int(landmark_coords[33][0]*x_size), int(landmark_coords[33][1]*y_size)), (int(landmark_coords[133][0]*x_size), int(landmark_coords[133][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(landmark_coords[160][0]*x_size), int(landmark_coords[160][1]*y_size)), (int(landmark_coords[144][0]*x_size), int(landmark_coords[144][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(landmark_coords[158][0]*x_size), int(landmark_coords[158][1]*y_size)), (int(landmark_coords[153][0]*x_size), int(landmark_coords[153][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(landmark_coords[362][0]*x_size), int(landmark_coords[362][1]*y_size)), (int(landmark_coords[263][0]*x_size), int(landmark_coords[263][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(landmark_coords[385][0]*x_size), int(landmark_coords[385][1]*y_size)), (int(landmark_coords[380][0]*x_size), int(landmark_coords[380][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(landmark_coords[387][0]*x_size), int(landmark_coords[387][1]*y_size)), (int(landmark_coords[373][0]*x_size), int(landmark_coords[373][1]*y_size)), (255, 0, 0))

            r_EAR = str("%.3f"%self.EAR(r_eye_coords))
            l_EAR = str("%.3f"%self.EAR(l_eye_coords))

            status = "Awake" if (self.EAR(r_eye_coords)+self.EAR(l_eye_coords))/2 >0.15 else "Drowsy"

            cv2.putText(image,r_EAR,org=(50,50),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(255,255,0),thickness=2)
            cv2.putText(image,l_EAR,org=(250,50),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(255,255,0),thickness=2)
            cv2.putText(image,status,org=(100,100),fontFace=cv2.FONT_HERSHEY_PLAIN,fontScale=1,color=(255,255,0),thickness=2)


        return image

    


