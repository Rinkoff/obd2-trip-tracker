import json
from dataclasses import asdict
from .models import TripReport

def print_report(report: TripReport):
    """Prints the report cleanly to standard output."""
    print("\n" + "="*40)
    print("          TRIP REPORT          ")
    print("="*40)
    print(f"Duration:          {report.duration_sec / 60:.1f} minutes ({report.duration_sec:.0f}s)")
    print(f"Start Odometer:    {report.start_odometer_km:.1f} km" if report.start_odometer_km else "Start Odometer:    N/A")
    print(f"End Odometer:      {report.end_odometer_km:.1f} km" if report.end_odometer_km else "End Odometer:      N/A")
    print(f"Distance Traveled: {report.distance_km:.2f} km" if report.distance_km else "Distance Traveled: N/A")
    print(f"Fuel Used (Est):   {report.fuel_used_l:.2f} L" if report.fuel_used_l else "Fuel Used (Est):   N/A")
    
    if report.avg_consumption_l_per_100km:
        print(f"Avg Consumption:   {report.avg_consumption_l_per_100km:.2f} L/100km")
    else:
        print("Avg Consumption:   N/A")
        
    print(f"Data Confidence:   {report.confidence}")
    
    print("\n--- Detected Issues ---")
    if report.issues:
        for issue in report.issues:
            print(f" - {issue}")
    else:
        print(" No issues detected. Smooth driving!")
    print("="*40 + "\n")

def save_report_json(report: TripReport, filepath: str = "trip_report.json"):
    """Saves the trip report as JSON."""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(report), f, indent=4)
        print(f"Report successfully saved to: {filepath}")
    except Exception as e:
        print(f"Failed to save JSON report: {e}")
