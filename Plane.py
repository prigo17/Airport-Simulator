import datetime
import random
import time


class Plane:
    def __init__(self, flight_number, arrival_time, plane_type="standard"):
        self.flight_number = flight_number
        self.arrival_time = arrival_time
        self.departure_time = arrival_time + datetime.timedelta(minutes=60 if plane_type != "large" else 90)
        self.assigned_runway = None
        self.status = "in air"  # in air, landed, taxiing, at gate, departing, departed
        self.passengers = random.randint(50, 200)
        self.delay_minutes = 0
        self.plane_type = plane_type  # standard, large, small

    def land(self):
        if self.assigned_runway:
            self.status = "landed"
            self.assigned_runway.release()
            self.assigned_runway = None
            self.status = "taxiing"
            time.sleep(1)  # Simulate taxiing
            self.status = "at gate"

    def depart(self):
        if self.status == "at gate" and self.assigned_runway:
            self.status = "taxiing"
            time.sleep(1)  # Simulate taxiing
            self.status = "departing"
            self.assigned_runway.release()
            self.assigned_runway = None
            self.status = "departed"

    def apply_delay(self, minutes):
        self.delay_minutes += minutes
        self.arrival_time += datetime.timedelta(minutes=minutes)