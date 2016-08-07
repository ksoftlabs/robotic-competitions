import cv2
import contour
import common


class PathQueue:

    # Path Queue (size: 100)
    # 99          0
    # .           .
    # .           .
    # .           .
    # 4                       9
    # 3                   7
    # 2       -2
    # 1   -5
    # 0           0

    def __init__(self, size):
        self.size = size
        self.items = [0.0] * self.size

    def enqueue(self, item):
        self.items.pop(0)
        self.items.append(item)

    def dequeue(self):
        self.items.append(0.0)
        return self.items.pop(0)

    def get_offset(self, index):
        if 0 <= index <= self.size - 1:
            return self.items[index]
        else:
            print 'Path index out of range'
            return None

    def clear(self):
        self.items = [0.0] * self.size


class Path:
    def __init__(self, robot, box):
        self.robot = robot
        self.box = box

        self.gray_img = None
        self.threshold_img = None

    def create_path(self):
        self.robot.processed_frame = self.refine_current_view()

        contours = common.get_contours(self.threshold_img)
        arrow_list = self.find_arrows(contours)

        for arrow in arrow_list:
            arrow.draw_initial_point(self.robot.processed_frame)
            arrow.draw_mid_base_point(self.robot.processed_frame)
            arrow.enable_lines(self.robot.processed_frame)
            arrow.enable_labels(self.robot.processed_frame)

        pass

    def refine_current_view(self):
        if self.box.color == 'red':
            canvas_frame = common.apply_mask(self.robot.current_frame, color='red')
        elif self.box.color == 'green':
            canvas_frame = common.apply_mask(self.robot.current_frame, color='green')
        elif self.box.color == 'blue':
            canvas_frame = common.apply_mask(self.robot.current_frame, color='blue')
        else:
            canvas_frame = common.apply_mask(self.robot.current_frame)

        self.gray_img = cv2.cvtColor(canvas_frame, cv2.COLOR_BGR2GRAY)
        self.threshold_img = common.get_otsu_gaussian_threshold(self.gray_img)

        return canvas_frame

    def find_arrows(self, contours):
        arrow_list = []
        for cnt in contours:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.01 * peri, True)
            cv2.drawContours(self.robot.processed_frame, [approx], -1, (255, 0, 0), 2)

            if len(approx) == 7:
                for i in range(7):
                    arrow = contour.Arrow(approx, i)
                    if arrow.is_valid_arrow():
                        arrow_list.append(arrow)
                        break

        return arrow_list
