import math 
from vessel import VesselType
from math import radians, sin, cos, sqrt, atan2

class VesselStateMachine:

    def __init__(self):
        self.time = 1
        self.radius = 10
        self.vessel = VesselType()
        self.spectator_vessel = VesselType()
        self.current_state = "start"

    def start(self):
        self.current_state = "wait_for_vessel"

    def wait_for_vessel(self):
        if is_vessel_in_range():
            self.current_state = "signal_captured"

    def signal_captured(self):
        position = None
        while True:
            if is_ais_signal_received():
                position = get_position_from_ais_signal(self.vessel)
                break
        self.current_state = "calculate_position"
        return position

    def calculate_position(self):
        if is_position_in_range(self, self.spectator_vessel, self.vessel, self.radius):
            if is_ais_signal_sent():
                self.current_state = "wait_for_vessel"
            else:
                self.current_state = "possible_dark_activity"
        else:
            self.current_state = "wait_for_vessel"

def is_vessel_in_range():
    # check if another vessel is in range
    pass

def is_ais_signal_received():
    #check if an AIS signal is received
    pass

def get_position_from_ais_signal(vessel: VesselType):
    return vessel.lat, vessel.lon

def calculate_estimated_position(vessel:VesselType, time):
    # calculate the estimated position of the vessel at time t+1
    heading = math.radians(vessel.heading)
    course = math.radians(vessel.course)

    speed = vessel.speed * 0.514444
    time = time * 3600
    distance = speed * time

    R = 6378000
    lat = math.radians(vessel.lat)
    lon = math.radians(vessel.lon)
    new_lat = math.asin(math.sin(lat) * math.cos(distance / R) + math.cos(lat) * math.sin(distance / R) * math.cos(heading))
    new_lon = lon + math.atan2(math.sin(heading) * math.sin(distance / R) * math.cos(lat), math.cos(distance / R) - math.sin(lat) * math.sin(new_lat))

    new_lat = math.degrees(new_lat)
    new_lon = math.degrees(new_lon)
    
    print(f"First Coordinates of {vessel.mmsi}: ({vessel.lat}, {vessel.lon})")
    print(f"Last Coordinates of {vessel.mmsi}: ({new_lat}, {new_lon})\n")
    return new_lat, new_lon

def is_position_in_range(self, spectator_vessel: VesselType, vessel: VesselType, radius):
    # check if the calculated position is in range
    new_lat, new_lon = calculate_estimated_position(vessel,self.time)
    new_lat_spectator, new_lon_spectator = calculate_estimated_position(spectator_vessel, self.time)

    # Calculate distance between the two coordinates using Haversine formula
    dlat = new_lat - new_lat_spectator
    dlon = new_lon - new_lon_spectator
    a = sin(dlat / 2) ** 2 + cos(new_lat_spectator) * cos(new_lat) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Earth's radius = 6371 km
    
    # check if the distance is within the radius
    return distance <= radius

def is_ais_signal_sent():
    # check if the vessel sent an AIS signal at time t+1
    pass

###############################################################

vessel_fsm = VesselStateMachine()

while True:
    if vessel_fsm.current_state == "start":
        vessel_fsm.start()
    elif vessel_fsm.current_state == "wait_for_vessel":
        vessel_fsm.wait_for_vessel()
    elif vessel_fsm.current_state == "signal_captured":
        position = vessel_fsm.signal_captured()
    elif vessel_fsm.current_state == "calculate_position":
        vessel_fsm.calculate_position(position)
    elif vessel_fsm.current_state == "possible_dark_activity":
        print("Possible dark activity detected")