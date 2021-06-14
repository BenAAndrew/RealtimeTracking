import time

MOVEMENT_MULTIPLIER = 5
SLEEP_TIME = 0.15
MIN_VALUE = 500
MAX_VALUE = 2500
RANGE = MAX_VALUE - MIN_VALUE


class Motor:
    def __init__(self, pin):
        self.pin = pin
        self.position = MIN_VALUE

    def change_position(self, pi, change):
        new_position = self.position + change
        if new_position >= MIN_VALUE and new_position <= MAX_VALUE:
            self.position = new_position
            pi.set_servo_pulsewidth(self.pin, self.position)
        else:
            print(f"{new_position} outside range")

    def close(self, pi):
        pi.set_servo_pulsewidth(self.pin, 0)


def send_position_to_motors(face, pi, pan, half_width, half_height):
    x, y, w, h = face
    centre_x = int(x + w / 2)
    # centre_y = int(y + h / 2)
    x_diff = half_width - centre_x
    # y_diff = half_height - centre_y
    print(x_diff)
    pan.change_position(pi, x_diff * MOVEMENT_MULTIPLIER)
    time.sleep(SLEEP_TIME)
