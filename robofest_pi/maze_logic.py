class Maze:
    def __init__(self, robot):
        self.robot = robot
        self.path_width = 30
        self.front_gap = (self.path_width - robot.length) / 2.0

    def is_on_junction(self):
        return self.is_left_open() or self.is_right_open()

    def is_on_end(self):
        return (not self.is_left_open()) and (not self.is_front_open()) and (not self.is_right_open())

    def is_left_open(self):
        return self.robot.left_sonar >= self.path_width

    def is_front_open(self):
        return self.robot.front_sonar >= self.front_gap

    def is_right_open(self):
        return  self.robot.right_sonar >= self.path_width
