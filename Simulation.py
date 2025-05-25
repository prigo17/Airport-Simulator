import datetime
import random

from Airport import parse_datetime_input
from Plane import Plane

class Simulation:
    def __init__(self, airport, simulation_hours=24):
        self.airport = airport
        self.current_time = datetime.datetime.now()
        self.simulation_end_time = self.current_time + datetime.timedelta(hours=simulation_hours)
        self.running = True
        self.generate_base_schedule()

    def generate_base_schedule(self):
        # Generate a base schedule of flights for the day
        for i in range(10):  # Schedule 10 flights throughout the day
            flight_number = f"BASE{i+1}"
            arrival_time = self.current_time + datetime.timedelta(minutes=random.randint(30, 1440))
            plane_type = random.choice(["standard", "large", "small"])
            plane = Plane(flight_number, arrival_time, plane_type)
            self.airport.schedule_arrival(plane)
            print(f"Base flight {flight_number} scheduled for {arrival_time}")

    def advance_time(self, minutes):
        end_time = self.current_time + datetime.timedelta(minutes=minutes)
        while not self.airport.event_queue.empty() and self.running:
            event = self.airport.event_queue.get()
            if event.time > end_time:
                self.airport.event_queue.put(event)
                break
            self.current_time = event.time
            event.action()
            print(f"Event: {event.description} at {self.current_time}")
            if random.random() < 0.05:  # 5% chance of emergency per event
                self.airport.schedule_emergency()
            if self.airport.check_loss_condition():
                print("Reputation has dropped below 30%. Simulation lost!")
                self.running = False
                break
        self.current_time = end_time
        if self.current_time >= self.simulation_end_time and self.running:
            self.check_win_condition()

    def check_win_condition(self):
        if self.airport.reputation >= 70:
            print(f"Simulation ended successfully with reputation {self.airport.reputation}%! You win!")
        else:
            print(f"Simulation ended with reputation {self.airport.reputation}%. You did not meet the win condition.")
        self.running = False

    def view_status(self):
        status = self.airport.get_status()
        time_remaining = (self.simulation_end_time - self.current_time).total_seconds() / 3600
        print("\n--- Airport Status ---")
        print(f"Current Time: {self.current_time}")
        print(f"Time Remaining: {time_remaining:.2f} hours")
        print(f"Weather: {status['weather']}")
        print(f"Score: {status['score']}")
        print(f"Reputation: {status['reputation']}%")
        print("Runways:")
        for num, stat in status["runways"]:
            print(f"  Runway {num}: {stat}")
        print("Planes:")
        for flight, stat, runway in status["planes"]:
            print(f"  Flight {flight}: {stat}, Runway: {runway if runway is not None else 'None'}")

    def view_logs(self):
        print("\n--- Event Logs ---")
        for log in self.airport.logs[-10:]:
            print(log)

    def schedule_maintenance(self):
        try:
            runway_number = int(input("Enter runway number for maintenance: "))
            duration = int(input("Enter maintenance duration in minutes: "))
            self.airport.schedule_maintenance(runway_number, duration)
        except ValueError:
            print("Invalid input!")

    def run(self):
        print("Welcome to Airport Simulator!")
        print("Manage your airport for 24 hours to maintain a high reputation and achieve the win condition!")
        while self.running and self.current_time < self.simulation_end_time:
            print("\n--- Main Menu ---")
            print(f"Current Time: {self.current_time}")
            print("1. View airport status")
            print("2. Advance time")
            print("3. Schedule plane arrival")
            print("4. Schedule runway maintenance")
            print("5. View logs")
            print("6. Exit")
            choice = input("Choose an action: ")

            if choice == "1":
                self.view_status()
            elif choice == "2":
                try:
                    minutes = int(input("Advance time by how many minutes? "))
                    self.advance_time(minutes)
                except ValueError:
                    print("Invalid input!")
            elif choice == "3":
                flight_number = input("Enter flight number: ")
                arrival_time_str = input("Enter arrival time (e.g. '15:30', '2025-05-24 15:30'): ")
                plane_type = input("Enter plane type (standard, large, small): ").lower()
                if plane_type not in ["standard", "large", "small"]:
                    plane_type = "standard"
                try:
                    arrival_time = parse_datetime_input(arrival_time_str)
                    plane = Plane(flight_number, arrival_time, plane_type)
                    self.airport.schedule_arrival(plane)
                    print(f"Flight {flight_number} scheduled for {arrival_time}")
                except ValueError as e:
                    print(f"Invalid time format: {e}")
            elif choice == "4":
                self.schedule_maintenance()
            elif choice == "5":
                self.view_logs()
            elif choice == "6":
                self.running = False
                print(f"Simulation ended early. Final Reputation: {self.airport.reputation}%")
            else:
                print("Invalid choice!")