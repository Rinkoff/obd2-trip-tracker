import sys
from typing import Optional
import obd

class ObdClient:
    def __init__(self, port: Optional[str] = None):
        if obd is None:
            print("Error: python-obd is not installed.", file=sys.stderr)
            print("Please install it by running: pip install obd", file=sys.stderr)
            sys.exit(1)
        self.port = port
        self.connection = None

    def connect(self) -> bool:
        """Establishes connection to an OBD2 adapter."""
        print("Connecting to OBD2 adapter...")
        try:
            if self.port:
                self.connection = obd.OBD(self.port)
            else:
                self.connection = obd.OBD()

            if not self.connection.is_connected():
                print("Failed to connect to OBD2 adapter. Please check the connection and try again.")
                return False

            print(f"Connected successfully! Protocol: {self.connection.protocol_name()}")
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def get_val(self, command) -> Optional[float]:
        """Helper to get a float value from an OBD command, handling missing values gracefully."""
        if not self.connection:
            return None
        try:
            response = self.connection.query(command)
            if not response.is_null() and response.value is not None:
                # python-obd values carry physical units (pint magnitudes)
                if hasattr(response.value, "magnitude"):
                    return float(response.value.magnitude)
                return float(response.value)
        except Exception:
            pass
        return None

    def read_odometer(self) -> Optional[float]:
        """Attempts to read the odometer, falling back securely if not supported."""
        try:
            if hasattr(self.commands, 'ODOMETER'):
                return self.get_val(self.commands.ODOMETER)
        except Exception:
            pass
        return None

    @property
    def commands(self):
        """Returns OBD commands module for easy access."""
        return obd.commands
