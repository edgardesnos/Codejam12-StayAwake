class DrowsinessAlerter:

    def __init__(self):
        self.drowsiness_counter = 0

    def should_alert(self, is_drowsy):
        if is_drowsy:
            self.drowsiness_counter += 1
        else:
            self.drowsiness_counter = 0
        if self.drowsiness_counter > 40:
            self.alert_driver()
            self.drowsiness_counter = 0

    def alert_driver(self):
        print("aaaa")