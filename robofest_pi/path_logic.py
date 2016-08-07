import cv2
import contour
import common


class Path:
    def __init__(self, robot, box):
        self.robot = robot
        self.box = box

        self.refined_frame = None

    def create_path(self):
        self.refine_current_view()
        self.robot.processed_frame = self.refined_frame

        contours = common.get_contours(self.refined_frame)

        arrow_list = self.find_arrows(contours)

        for arrow in arrow_list:
            arrow.draw_initial_point(self.robot.processed_frame)
            arrow.draw_mid_base_point(self.robot.processed_frame)
            arrow.enable_lines(self.robot.processed_frame)
            arrow.enable_labels(self.robot.processed_frame)

    def refine_current_view(self):
        if self.box.color == 'red':
            canvas_frame = common.apply_mask(self.robot.current_frame, color='red')
        elif self.box.color == 'green':
            canvas_frame = common.apply_mask(self.robot.current_frame, color='green')
        elif self.box.color == 'blue':
            canvas_frame = common.apply_mask(self.robot.current_frame, color='blue')
        else:
            canvas_frame = common.apply_mask(self.robot.current_frame)

        gray_img = cv2.cvtColor(canvas_frame, cv2.COLOR_BGR2GRAY)
        threshold_img = common.get_otsu_gaussian_threshold(gray_img)

        self.refined_frame = threshold_img
        cv2.imshow('Threshold image', threshold_img)

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
