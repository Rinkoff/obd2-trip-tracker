from typing import List, Optional
from .models import Sample

def estimate_distance(samples: List[Sample]) -> Optional[float]:
    """Estimates distance by integrating speed over time if odometer fails."""
    if len(samples) < 2:
        return
    dist_km = 0.0
    for i in range(1, len(samples)):
        curr = samples[i]
        prev = samples[i - 1]
        if curr.speed_kph is not None:
            dt_hours = (curr.ts - prev.ts) / 3600.0
            dist_km += curr.speed_kph * dt_hours
    return dist_km if dist_km > 0 else None

def estimate_fuel(samples: List[Sample]) -> Optional[float]:
    """Estimates fuel consumption from Mass Air Flow (MAF) sensor data."""
    total_fuel_l = 0.0
    valid_samples = 0
    
    for i in range(1, len(samples)):
        prev = samples[i - 1]
        curr = samples[i]
        if curr.maf_gps is not None:
            dt_sec = curr.ts - prev.ts
            fuel_mass_grams = (curr.maf_gps / 14.7) * dt_sec
            fuel_volume_l = fuel_mass_grams / 740.0
            total_fuel_l += fuel_volume_l
            valid_samples += 1
            
    if valid_samples > 0:
        return total_fuel_l
    return None

def detect_issues(samples: List[Sample]) -> List[str]:
    """Detects simple heuristic-based driving issues."""
    issues = set()
    idle_time = 0.0
    
    for i in range(1, len(samples)):
        prev = samples[i - 1]
        curr = samples[i]
        dt = curr.ts - prev.ts

        # High RPM at low speed
        if curr.rpm is not None and curr.speed_kph is not None:
            if curr.rpm > 3500 and curr.speed_kph < 30:
                issues.add("High RPM at low speed detected.")
                
        # Aggressive throttle bursts
        if curr.throttle is not None and prev.throttle is not None and dt > 0:
            delta_throttle_per_sec = (curr.throttle - prev.throttle) / dt
            if delta_throttle_per_sec > 40:  # >40% throttle change within a second
                issues.add("Frequent hard acceleration.")
                
        # Long idle
        if curr.speed_kph is not None and curr.speed_kph < 3:
            if curr.rpm is not None and curr.rpm > 300:
                idle_time += dt
                if idle_time > 180:  # 3 minutes of idling
                    issues.add("Possible long idle.")
        else:
            idle_time = 0.0
            
    return sorted(list(issues))
