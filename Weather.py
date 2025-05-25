import datetime
import random


class Weather:
    def __init__(self):
        self.condition = "clear"  # clear, stormy, foggy
        self.next_change = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 120))

    def update(self):
        if datetime.datetime.now() >= self.next_change:
            self.condition = random.choice(["clear", "stormy", "foggy"])
            self.next_change = datetime.datetime.now() + datetime.timedelta(minutes=random.randint(30, 120))

    def affect_operations(self):
        if self.condition == "stormy":
            return "delays"
        elif self.condition == "foggy":
            return "reduced visibility"
        return "normal"