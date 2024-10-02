from threading import Timer
import time

class CustomTimer:
    def __init__(self):
        self.timer = None
        self.starting_time = None
        self.waiting_time = None

    # If timer not created: create and start
    # if already created: calculate remaining timer time and create new timer with remaining + new seconds
    def start(self, seconds: int, func) -> None:
        if self.timer is None:
            self.waiting_time = seconds
            self.timer = Timer(self.waiting_time, func)
            self.starting_time = int(time.time())
            self.timer.start()
            
        else:
            # Calculate new waiting time
            now = int(time.time())
            old_final_time = self.starting_time + self.waiting_time
            remaining_time = old_final_time - now
            new_waiting_time = remaining_time + seconds

            # Create noe timer with calculated waiting time
            self.timer.cancel()
            self.timer = Timer(new_waiting_time, func)
            self.timer.start()

            # Reset variables
            self.starting_time = now
            self.waiting_time = new_waiting_time
            

    def stop(self):
        if self.timer is not None:
            self.timer.cancel()
        self.timer = None

    def get_remaining_minutes(self) -> int:
        if self.timer is None:
            return 0
        remaining_minutes = int(((self.starting_time + self.waiting_time) - int(time.time()))/60)
        return remaining_minutes if remaining_minutes > 0 else 0
