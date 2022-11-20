import mediapipe as mp
import cv2

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

    def detect_mesh(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                test_list = [(d.x, d.y, d.z) for d in face_landmarks.landmark]
                #test_list.append(face_landmarks)
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
                self.mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=self.mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=self.mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style()
                )
            y_size, x_size, _ = image.shape
            image = cv2.line(image, (int(test_list[33][0]*x_size), int(test_list[33][1]*y_size)), (int(test_list[133][0]*x_size), int(test_list[133][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(test_list[160][0]*x_size), int(test_list[160][1]*y_size)), (int(test_list[144][0]*x_size), int(test_list[144][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(test_list[158][0]*x_size), int(test_list[158][1]*y_size)), (int(test_list[153][0]*x_size), int(test_list[153][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(test_list[362][0]*x_size), int(test_list[362][1]*y_size)), (int(test_list[263][0]*x_size), int(test_list[263][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(test_list[385][0]*x_size), int(test_list[385][1]*y_size)), (int(test_list[380][0]*x_size), int(test_list[380][1]*y_size)), (255, 0, 0))
            image = cv2.line(image, (int(test_list[387][0]*x_size), int(test_list[387][1]*y_size)), (int(test_list[373][0]*x_size), int(test_list[373][1]*y_size)), (255, 0, 0))
        
        return image

