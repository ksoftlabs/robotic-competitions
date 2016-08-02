class Port:
    def __init__(self):
        print 'Initializing port communication....'

    def send(self, data):
        print data

    def change_speed(self, lf, rf, lb, rb):
        command = '[s ' + str(lf) + ' ' + str(rf) + ' ' + str(lb) + ' ' + str(rb) + ']'
        self.send(command)

    def get_front_distance(self):
        pass

    def get_left_distance(self):
        pass

    def get_right_distance(self):
        pass

    def get_back_direction(self):
        pass
