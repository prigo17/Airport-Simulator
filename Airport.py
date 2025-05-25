import datetime
import queue
import random

from dateutil.parser import parse

from Event import Event
from Plane import Plane
from Runway import Runway
from Weather import Weather


class Airport:
    def __init__(self, num_runways):
        self.runways = [Runway(i) for i in range(num_runways)]
        self.planes = []
        self.event_queue = queue.PriorityQueue()
        self.logs = []
        self.weather = Weather()
        self.score = 0
        self.reputation = 100  # Start with 100% reputation

    def schedule_arrival(self, plane):
        self.planes.append(plane)
        arrival_event = Event(
            plane.arrival_time,
            lambda: self.handle_arrival(plane),
            f"Flight {plane.flight_number} arriving"
        )
        self.event_queue.put(arrival_event)
        if plane.departure_time:
            departure_event = Event(
                plane.departure_time,
                lambda: self.handle_departure(plane),
                f"Flight {plane.flight_number} departing"
            )
            self.event_queue.put(departure_event)

    def handle_arrival(self, plane):
        self.weather.update()
        weather_effect = self.weather.affect_operations()
        if weather_effect == "delays" or random.random() < 0.1:  # 10% chance of random delay
            delay = random.randint(10, 60)
            plane.apply_delay(delay)
            self.logs.append(f"{plane.flight_number} delayed by {delay} minutes due to {weather_effect or 'random event'} at {datetime.datetime.now()}")
            self.schedule_arrival(plane)
            self.score -= 5
            self.reputation = max(0, self.reputation - 2)  # Decrease reputation
            return
        available_runways = [r for r in self.runways if r.status == "available" and (self.weather.condition != "foggy" or r.number < len(self.runways) // 2)]
        for runway in available_runways:
            runway.update_status()
            if runway.assign_plane(plane):
                plane.land()
                self.logs.append(f"{plane.flight_number} landed on Runway {runway.number} at {datetime.datetime.now()}")
                self.score += 10
                self.reputation = min(100, self.reputation + 1)  # Increase reputation
                break
        else:
            self.logs.append(f"No runway available for {plane.flight_number} at {datetime.datetime.now()}")
            self.score -= 5
            self.reputation = max(0, self.reputation - 2)  # Decrease reputation

    def handle_departure(self, plane):
        if plane.status != "at gate":
            return
        for runway in self.runways:
            runway.update_status()
            if runway.assign_plane(plane):
                plane.depart()
                self.logs.append(f"{plane.flight_number} departed from Runway {runway.number} at {datetime.datetime.now()}")
                self.score += 10
                self.reputation = min(100, self.reputation + 1)  # Increase reputation
                break
        else:
            self.logs.append(f"No runway for {plane.flight_number} departure at {datetime.datetime.now()}")
            self.score -= 5
            self.reputation = max(0, self.reputation - 2)  # Decrease reputation

    def schedule_emergency(self):
        flight_number = f"EM{random.randint(100, 999)}"
        plane = Plane(flight_number, datetime.datetime.now() + datetime.timedelta(minutes=random.randint(5, 15)), plane_type="small")
        self.schedule_arrival(plane)
        self.logs.append(f"Emergency flight {flight_number} scheduled at {datetime.datetime.now()}")

    def get_status(self):
        status = {
            "runways": [(r.number, r.status) for r in self.runways],
            "planes": [(p.flight_number, p.status, p.assigned_runway.number if p.assigned_runway else None) for p in self.planes],
            "weather": self.weather.condition,
            "score": self.score,
            "reputation": self.reputation
        }
        return status

    def check_loss_condition(self):
        if self.reputation < 30:
            return True
        return False

def parse_datetime_input(dt_str, default_date=None):
    try:
        if len(dt_str.strip().split()) == 1 and dt_str.count(":") == 1:
            time_part = dt_str.strip()
            date_part = (default_date or datetime.date.today()).isoformat()
            dt_str = f"{date_part} {time_part}"
        return parse(dt_str)
    except Exception as e:
        raise ValueError(f"Could not parse date/time '{dt_str}': {e}")