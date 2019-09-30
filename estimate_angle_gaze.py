import math
import dlib
import cv2
import numpy as np
from imutils import  face_utils
from text import text
from text import text
from threading import Thread
from queue import Queue
import time
from noti import noti


class Angle_horizontal:

    def __init__(self, point_x):

        self.point_x = point_x
        self.horizontal_px = 320
        self.horizontal_cm = 59.8316
        self.adjecent_side = 193.4
        self.new_point_x = 0

    def change_point_start_horizontal(self):

        if self.point_x < self.horizontal_px: # make index gaze
            self.status_gaze = "RIGHT"
        else:
            self.status_gaze = "LEFT"

        self.new_point_x = abs(self.point_x - self.horizontal_px)  # new point start 0 center

        return self.new_point_x, self.status_gaze

    def estimate_angle_horizontal(self):

        self.W = self.horizontal_px / self.horizontal_cm # scale cm : px
        self.eye_weight_cm = self.new_point_x / self.W # weight cm eye point
        self.angle_weight = (math.atan2(self.eye_weight_cm, self.adjecent_side) * 180 / math.pi) # calculator angle by arctan

        return self.angle_weight, self.eye_weight_cm, self.W

class Angle_vertical:

    def __init__(self, point_y, re_inches=0):

        self.point_y = point_y
        self.re_inches = re_inches
        self.vertical_px = 240
        self.vertical_cm = 46.9785
        self.adjecent_side = 193.4
        self.px_plus = 13.33  # 240/18"
        self.cm_plus = 2.54  # inch : cm
        self.new_point_y = 0
        self.vertical_px_new = 0
        self.vertical_cm_new = 0

    def set_camera(self):

        self.vertical_px_new = self.vertical_px + (self.px_plus * self.re_inches)
        self.vertical_cm_new = self.vertical_cm + (self.cm_plus * self.re_inches)

        return self.vertical_px_new, self.vertical_cm_new

    def change_point_start_vertical(self):

        if self.point_y < self.vertical_px_new :
            self.status_gaze = "UP"
        else:
            self.status_gaze = "DOWN"

        self.new_point_y = abs(self.point_y - self.vertical_px_new)

        return self.new_point_y , self.status_gaze

    def estimate_angle_vertical(self):

        self.H = self.vertical_px_new  / self.vertical_cm_new
        self.eye_height_cm = self.new_point_y / self.H
        self.angle_height = (math.atan2(self.eye_height_cm, self.adjecent_side) * 180 / math.pi)

        return self.angle_height, self.eye_height_cm, self.H

class Extand_eyes:
    def __init__(self):

        # Dlib function call model
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(
            r'data/shape_predictor_68_face_landmarks.dat')

        # Indexes facial landmarks
        (self.left_eye_Start, self.left_eye_End) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.right_eye_Start, self.right_eye_End) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # Extend from dlib point
    def extend(self,image_gray):

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

            return {
                    "center_right_x": self.center_right_x,
                    "center_right_y": self.center_right_y,
                    "center_left_x": self.center_left_x,
                    "center_left_y": self.center_left_y,
                    "point_center_x": self.point_center_x,
                    "point_center_y": self.point_center_y,
                    "rightEye": self.rightEye,
                    "leftEye": self.leftEye
                    }

queue_h = Queue()
queue_h_view = Queue()
queue_v = Queue()
queue_v_view = Queue()

# Thread method
def notific_angle():

    item_h = queue_h.get()
    item_h_view = queue_h_view.get()
    item_v = queue_v.get()
    item_v_view = queue_v_view.get()
    noti("ANGLE GAZE RISK", "you gaze horizontal {:.2f} {} vertical {:.2f} {}".format(  item_h, 
                                                                                        item_h_view, 
                                                                                        item_v, 
                                                                                        item_v_view))
                                                                                        
# Start thread method
def start_notific_angle(h, h_view, v, v_view):

    queue_h.put(h)
    queue_h_view.put(h_view)
    queue_v.put(v)
    queue_v_view.put(v_view)
    th_angle_notifi = Thread(target=notific_angle)
    th_angle_notifi.start()

# Draw line in app
def draw_line_in_app(im, list_line):

    for i in list_line:
        cv2.line(im, i["pt1"], i["pt2"], i["color"], i["sizeline"])
    
    return im

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)
    eyes = Extand_eyes()
    horizotal = ""
    vertical = ""
    num_frame = 0

    while True:

        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eye = eyes.extend(gray)

        num_frame += 1

        try:
            # Cal vertical
            point_x = eye["point_center_x"]
            angle_horizotal = Angle_horizontal(point_x)
            status_horizotal = angle_horizotal.change_point_start_horizontal()
            horizotal = angle_horizotal.estimate_angle_horizontal()

            # Cal horisotal
            point_y = eye["point_center_y"]
            angle_vertical = Angle_vertical(point_y, 5)
            angle_vertical.set_camera()
            status_vertical = angle_vertical.change_point_start_vertical()
            vertical = angle_vertical.estimate_angle_vertical()

            # DRAW LINE AND TEXT
            # List line for build
            line_list_build = [ {"pt1":(320, 0), "pt2":(320, 480), "color":(255, 255, 255), "sizeline": 1},
                                {"pt1":(0, int(angle_vertical.set_camera()[0])), "pt2":(640, int(angle_vertical.set_camera()[0])), "color":(255, 255, 255), "sizeline": 1},
                                {"pt1":(int(eye["point_center_x"]), 0), "pt2":(int(eye["point_center_x"]), 480), "color":(0, 0, 255), "sizeline": 1},
                                {"pt1":(0, int(eye["point_center_y"])), "pt2":(640, int(eye["point_center_y"])), "color":(0, 0, 255), "sizeline": 1},
                                ]

            # List text for build
            text_list_build = [
                                {"roi":(int(eye["point_center_x"]) + 15, 5), "text": "{:.2f} {}".format(horizotal[0], status_horizotal[1]), "size": 18, "color": (0, 0, 0)},
                                {"roi":(15, int(eye["point_center_y"]) + 5), "text": "{:.2f} {}".format(vertical[0], status_vertical[1]), "size": 18, "color": (0, 0, 0)}
                                ]

            # Build line
            draw_line_in_app(frame, line_list_build)

            # Build text
            for i_text in text_list_build:
                frame = text(frame, i_text["roi"], i_text["text"], i_text["size"], i_text["color"])

            # STAMENT ALERT FOR NOTIC NOT RULE CVS
            if num_frame % 50 == 0: 

                if status_vertical[1] == "UP" and vertical[0] >= 8 and horizotal[0] <= 6:
                    print("++++++++++++++++++++++++++++++++")
                    print("GOOD VIEW")
                    pass
                else:
                    print("--------------------------------")
                    print("BAD VIEW")
                    start_notific_angle(horizotal[0], status_horizotal[1], vertical[0], status_vertical[1])

            print(f'horizotal({status_horizotal[1]}) : {horizotal[0]:.2f} vertical({status_vertical[1]}) : {vertical[0]:.2f}')

        except:
            print("No find face")

        cv2.imshow('out', frame)

        if cv2.waitKey(1) == 27 or cv2.getWindowProperty('out', 1) == -1:
            break