import time
import random
import math
from typing import Optional

class MockCommands:
    SPEED = "SPEED"
    RPM = "RPM"
    THROTTLE_POS = "THROTTLE_POS"
    ENGINE_LOAD = "ENGINE_LOAD"
    MAF = "MAF"
    ODOMETER = "ODOMETER"

class MockObdClient:
    """A simulated OBD client that generates fake car data for testing."""
    def __init__(self):
        self.connected = False
        self.start_time = time.time()
        self.commands = MockCommands()
        self.base_odometer = 120500.0

    def connect(self) -> bool:
        print("Connecting to MOCK OBD2 adapter...")
        time.sleep(1)
        self.connected = True
        print("Connected successfully! Protocol: MOCK-ELM327")
        return True

    def get_val(self, command) -> Optional[float]:
        if not self.connected:
            return None
            
        elapsed = time.time() - self.start_time
        
        # Simulate realistic driving dynamics based on time elapsed
        if command == self.commands.SPEED:
            # Vary speed up and down (e.g. accelerating and braking)
            speed = abs(40.0 * math.sin(elapsed / 10.0)) + random.uniform(0, 5)
            return speed
        elif command == self.commands.RPM:
            # RPM correlates roughly with speed + idle
            rpm = 800.0 + abs(2500.0 * math.sin(elapsed / 10.0)) + random.uniform(-100, 200)
            # Add some simulated issues: High RPM at low speed sometimes
            if random.random() < 0.05:  # 5% chance
                rpm = 4000.0
            return rpm
        elif command == self.commands.THROTTLE_POS:
            throttle = abs(50.0 * math.cos(elapsed / 10.0)) + random.uniform(0, 10)
            return throttle
        elif command == self.commands.ENGINE_LOAD:
            return random.uniform(20.0, 70.0)
        elif command == self.commands.MAF:
            # MAF loosely correlates with RPM
            return random.uniform(2.0, 30.0)
            
        return None

    def read_odometer(self) -> Optional[float]:
        if not self.connected:
            return None
        # Add some distance based on elapsed time (e.g. driving at ~30km/h average)
        elapsed_hours = (time.time() - self.start_time) / 3600.0
        return self.base_odometer + (elapsed_hours * 30.0)
