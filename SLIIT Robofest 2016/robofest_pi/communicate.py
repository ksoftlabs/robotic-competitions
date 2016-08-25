class Port:
    def __init__(self):
        print 'Initializing port communication....'

    def send(self, data):
        print data

    def change_speed(self, lf, rf, lb, rb):
        command = '[s ' + str(lf) + ' ' + str(rf) + ' ' + str(lb) + ' ' + str(rb) + ']'
        self.send(command)

    def get_front_distance(self):
        print "Getting front sonar data...."

    def get_left_distance(self):
        print "Getting left sonar data...."

    def get_right_distance(self):
        print "Getting right sonar data...."

    def get_back_direction(self):
        print "Getting back sonar data...."
