import physics
import communicate

class Decision:
    def __init__(self, robot):
        self.comm = communicate.Port()
        self.robot = physics.Robot()

    def get_sonar_data(self):
