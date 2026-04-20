import time
from typing import List, Optional
from .models import Sample, TripReport
from .client import ObdClient
from . import analyzer

class ObdTripTracker:
    def __init__(self, port: Optional[str] = None, simulate: bool = False):
        if simulate:
            from .mock_client import MockObdClient
            self.client = MockObdClient()
        else:
            self.client = ObdClient(port=port)
        self.samples: List[Sample] = []
        self.start_ts: Optional[float] = None
        self.end_ts: Optional[float] = None
        self.start_odometer: Optional[float] = None
        self.end_odometer: Optional[float] = None

    def connect(self) -> bool:
        """Proxies connection attempt to the client."""
        return self.client.connect()

    def capture_start(self):
        """Marks the start of the trip."""
        print("\nStarting trip...")
        self.start_ts = time.time()
        self.start_odometer = self.client.read_odometer()
        if self.start_odometer is None:
            print("Note: Odometer reading not supported by vehicle. Distance will be estimated.")

    def capture_sample(self):
        """Polls standard PIDs and saves a single sample in memory."""
        cmds = self.client.commands
        sample = Sample(
            ts=time.time(),
            speed_kph=self.client.get_val(cmds.SPEED),
            rpm=self.client.get_val(cmds.RPM),
            throttle=self.client.get_val(cmds.THROTTLE_POS),
            engine_load=self.client.get_val(cmds.ENGINE_LOAD),
            maf_gps=self.client.get_val(cmds.MAF)
        )
        self.samples.append(sample)

    def build_report(self) -> TripReport:
        """Processes collected data and builds the final Trip Report."""
        distance_km = None
        confidence = "High"

        # distance
        if self.start_odometer is not None and self.end_odometer is not None:
            distance_km = self.end_odometer - self.start_odometer
        else:
            distance_km = analyzer.estimate_distance(self.samples)
            confidence = "Low (Estimated from Vehicle Speed fallback)"

        # fuel
        fuel_used_l = analyzer.estimate_fuel(self.samples)
        
        # average consumption
        avg_consumption = None
        if distance_km and distance_km > 0 and fuel_used_l is not None:
            avg_consumption = (fuel_used_l / distance_km) * 100
        
        # duration
        duration = 0.0
        if self.start_ts is not None and self.end_ts is not None:
            duration = self.end_ts - self.start_ts

        return TripReport(
            start_odometer_km=self.start_odometer,
            end_odometer_km=self.end_odometer,
            distance_km=distance_km,
            fuel_used_l=fuel_used_l,
            avg_consumption_l_per_100km=avg_consumption,
            issues=analyzer.detect_issues(self.samples),
            confidence=confidence,
            duration_sec=duration
        )
