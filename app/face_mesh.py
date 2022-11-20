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

        # Useful mesh point indices for calculating eye aspect ratio
        self.eye_landmarks = [33, 133, 160, 144, 158, 153, 362, 263, 385, 380, 387, 373]

    def get_eye_aspect_ratio(self, eye_landmarks):
        """Compute the eye aspect ratio"""
        horizontal = distance.euclidean(eye_landmarks[0], eye_landmarks[1])
        vertical_1 = distance.euclidean(eye_landmarks[2], eye_landmarks[3])
        vertical_2 = distance.euclidean(eye_landmarks[4], eye_landmarks[5])

        ear = (vertical_1 + vertical_2) / (2* horizontal)

        return ear

    def detect_mesh(self, image):
        """Adds mesh to the image and returns eye coordinates with it."""
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        is_drowsy = False
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

            eye_coords = [(landmark_coords[index][0],landmark_coords[index][1]) for index in self.eye_landmarks]

            image = self.draw_eye_lines(image, eye_coords)

            drowsiness, ear_right, ear_left = self.get_drowsiness_level(eye_coords)

            is_drowsy = drowsiness < 0.15

            image = self.display_drowsiness(image, is_drowsy, ear_right, ear_left)

        return image, is_drowsy

    def display_drowsiness(self, image, is_drowsy, ear_right, ear_left):
        status = "Drowsy" if is_drowsy else "Awake"
        cv2.putText(image, f"{ear_right:.3f}", org=(50,50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255,255,0), thickness=2)
        cv2.putText(image, f"{ear_left:.3f}", org=(250,50), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255,255,0), thickness=2)
        cv2.putText(image, status, org=(100,100), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255,255,0), thickness=2)
        return image


    def get_drowsiness_level(self, eye_coords):
        """Compute the drowsiness level and ear for both eyes."""
        ear_right = self.get_eye_aspect_ratio(eye_coords[:6])
        ear_left = self.get_eye_aspect_ratio(eye_coords[6:])
        drowsiness = (ear_right + ear_left) / 2
        return drowsiness, ear_right, ear_left


    def draw_eye_lines(self, image, eye_coords):
        y_length, x_length, _ = image.shape
        for i in range(0, len(eye_coords), 2):
            point1 = (int(eye_coords[i][0] * x_length), int(eye_coords[i][1] * y_length))
            point2 = (int(eye_coords[i+1][0] * x_length), int(eye_coords[i+1][1] * y_length))
            image = cv2.line(image, point1, point2, (255, 0, 0))
        return image

    


