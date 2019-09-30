import math

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

def estimate_distance(angle_height, H)

    Radiansx = math.radians(abs(90 - angle_height))
    tanx = math.tan(Radiansx)

    return tanx*H
