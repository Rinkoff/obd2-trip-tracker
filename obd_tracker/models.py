from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Sample:
    ts: float
    speed_kph: Optional[float]
    rpm: Optional[float]
    throttle: Optional[float]
    engine_load: Optional[float]
    maf_gps: Optional[float]

@dataclass
class TripReport:
    start_odometer_km: Optional[float]
    end_odometer_km: Optional[float]
    distance_km: Optional[float]
    fuel_used_l: Optional[float]
    avg_consumption_l_per_100km: Optional[float]
    issues: List[str]
    confidence: str
    duration_sec: float
