import dlib
import imutils
from imutils import face_utils


class Extract_eyes:
    
    def __init__(self):

        # Dlib function call model
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            r'data/shape_predictor_68_face_landmarks.dat')

        # Indexes facial landmarks
        (self.left_eye_Start, self.left_eye_End) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.right_eye_Start, self.right_eye_End) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # Extract from dlib point
    @staticmethod
    def extract(self,image_gray):

        self.detect_from_model = self.detector(image_gray, 0)

        for self.rect in self.detect_from_model:
            # Detect & convert numpy
            self.shape = self.predictor(image_gray, self.rect)
            self.shape = face_utils.shape_to_np(self.shape)

            # Extend for eye aspect ratio
            self.leftEye = self.shape[self.left_eye_Start: self.left_eye_End]
            self.rightEye = self.shape[self.right_eye_Start: self.right_eye_End]

            self.right_x_0, self.right_y_0 = self.rightEye[0]
            self.right_x_3, self.right_y_3 = self.rightEye[3]

            self.left_x_0, self.left_y_0 = self.leftEye[0]
            self.left_x_3, self.left_y_3 = self.leftEye[3]

            # Def  x and y eye center
            self.right_x = abs(self.right_x_0 - self.right_x_3) / 2
            self.right_y = abs(self.right_y_0 - self.right_y_3) / 2
            self.left_x = (self.left_x_3 - self.left_x_0) / 2
            self.left_y = (self.left_y_3 - self.left_y_0) / 2

            # Fix center eyes right and left
            self.center_right_x = self.right_x_0 + self.right_x
            self.center_right_y = self.right_y_0 + self.right_y

            self.center_left_x = self.left_x_0 + self.right_x
            self.center_left_y = self.left_y_0 + self.right_y

            self.point_center_x = (self.center_right_x + self.center_left_x) / 2
            self.point_center_y = (self.center_right_y + self.center_left_y) / 2

            # Return eye ROI
            return {
                    "eye_right" : (self.center_right_x, self.center_right_y),
                    "eye_left"  : (self.center_left_x, self.center_left_y),
                    "eye_center": (self.point_center_x, self.point_center_y)
                    }