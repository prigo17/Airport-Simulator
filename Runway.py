import datetime


class Runway:
    def __init__(self, number):
        self.number = number
        self.status = "available"  # available, occupied, maintenance
        self.maintenance_end = None

    def assign_plane(self, plane):
        if self.status == "available":
            self.status = "occupied"
            plane.assigned_runway = self
            return True
        return False

    def release(self):
        self.status = "available"

    def start_maintenance(self, duration_minutes):
        self.status = "maintenance"
        self.maintenance_end = datetime.datetime.now() + datetime.timedelta(minutes=duration_minutes)

    def update_status(self):
        if self.status == "maintenance" and datetime.datetime.now() >= self.maintenance_end:
            self.status = "available"
            self.maintenance_end = None