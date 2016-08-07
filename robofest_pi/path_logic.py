import cv2
import contour
import common


class Path:
    def __init__(self, robot, path_queue, box):
        self.robot = robot
        self.path_queue = path_queue
        self.box = box

        self.frame_width = self.robot.get_frame_width()

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

            # Change path queue
            m = arrow.get_main_axis_gradient()
            c = arrow.get_main_axis_intercept()
            a = min([arrow.in2y, arrow.midy])
            b = max([arrow.in2y, arrow.midy])
            for y in range(a, b + 1):
                if m == 0.0:        # >>>>>>>>>>>>>>>>>>>>> Has to check how the robot responds to horizontal arrows
                    if arrow.in2x > arrow.midx:     # points East
                        x = self.frame_width
                    else:                           # Points West
                        x = 0
                elif m == float('Inf') or m == float('-Inf'):
                    x = (arrow.in2x + arrow.midx) / 2.0
                else:
                    x = y - c / m

                self.path_queue.set_offset(y, x)

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
