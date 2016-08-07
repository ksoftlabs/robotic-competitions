import cv2
import common


class Arrow:
    def __init__(self, point_set, pos):             # pos is the position of the required point (starting position)
        self.pos = pos

        self.i0x = point_set[pos][0][0]
        self.i0y = point_set[pos][0][1]
        self.i1x = point_set[(pos + 1) % 6][0][0]
        self.i1y = point_set[(pos + 1) % 6][0][1]
        self.i2x = point_set[(pos + 2) % 6][0][0]
        self.i2y = point_set[(pos + 2) % 6][0][1]
        self.i3x = point_set[(pos + 3) % 6][0][0]
        self.i3y = point_set[(pos + 3) % 6][0][1]

        if pos == 0:
            self.in2x = point_set[5][0][0]
            self.in2y = point_set[5][0][1]
        elif pos == 1:
            self.in2x = point_set[6][0][0]
            self.in2y = point_set[6][0][1]
        else:
            self.in2x = point_set[pos - 2][0][0]
            self.in2y = point_set[pos - 2][0][1]

        self.midx = (self.i1x + self.i2x) / 2
        self.midy = (self.i1y + self.i2y) / 2

    def is_valid_arrow(self):
        m1 = self.get_i0_to_i1_gradient()
        m2 = self.get_i2_to_i3_gradient()

        d1 = self.get_i0_to_i1_distance()
        d2 = self.get_i2_to_i3_distance()

        return abs(m1 - m2) <= 0.5 and abs(d1 - d2) <= 15

    def get_i0_to_i1_gradient(self):
        return common.get_gradient(self.i0x, self.i0y, self.i1x, self.i1y)

    def get_i2_to_i3_gradient(self):
        return common.get_gradient(self.i2x, self.i2y, self.i3x, self.i3y)

    def get_i0_to_i1_distance(self):
        return common.get_distance(self.i0x, self.i0y, self.i1x, self.i1y)

    def get_i2_to_i3_distance(self):
        return common.get_distance(self.i2x, self.i2y, self.i3x, self.i3y)

    def draw_initial_point(self, frame, radius=4, color=(0, 255, 0), thickness=2):
        cv2.circle(frame, (self.i0x, self.i0y), radius, color, thickness)

    def draw_mid_base_point(self, frame, radius=4, color=(0, 255, 0), thickness=2):
        cv2.circle(frame, (self.midx, self.midy), radius, color, thickness)

    def enable_lines(self, frame):
        cv2.line(frame, (self.midx, self.midy), (self.in2x, self.in2y), (0, 255, 0), 2)
        cv2.line(frame, (self.i0x, self.i0y), (self.i1x, self.i1y), (255, 255, 255), 2)
        cv2.line(frame, (self.i2x, self.i2y), (self.i3x, self.i3y), (255, 255, 255), 2)

    def enable_labels(self, frame):
        cv2.putText(frame, str(self.pos), (self.i0x + 10, self.i0y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
        cv2.putText(frame, str(self.pos + 1), (self.i1x + 10, self.i1y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
        cv2.putText(frame, str(self.pos + 2), (self.i2x + 10, self.i2y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
        cv2.putText(frame, str(self.pos + 3), (self.i3x + 10, self.i3y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
        cv2.putText(frame, str('HEAD'), (self.in2x + 10, self.in2y + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
        cv2.putText(frame, str('BASE'), (self.midx + 10, self.midy + 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.8,
                    (255, 255, 255))
