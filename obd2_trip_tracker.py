"""
OBD2 Trip Tracker - Console MVP
A simple CLI application that reads data from an OBD2 ELM327 adapter,
tracks a trip, and generates a report.
"""

import time
import argparse
import sys

from obd_tracker.tracker import ObdTripTracker
from obd_tracker.reporter import print_report, save_report_json

def main():
    parser = argparse.ArgumentParser(description="OBD2 Console-Only Trip Tracker MVP")
    parser.add_argument("--port", type=str, help="Optional serial port for OBD2 adapter (e.g. /dev/ttyUSB0, COM3)")
    args = parser.parse_args()

    tracker = ObdTripTracker(port=args.port)
    
    print("Initializing OBD2 Trip Tracker...")
    if not tracker.connect():
        print("OBD2 adapter not found. Exiting application...")
        return

    try:
        input("Press [ENTER] when ready to start the trip...")
    except KeyboardInterrupt:
        print("Aborted before starting.")
        return

    tracker.capture_start()
    
    print("Trip started! Collecting OBD2 samples every 2 seconds...")
    print(">>> Press [Ctrl+C] to STOP the trip and generate your report. <<<")
    
    try:
        while True:
            tracker.capture_sample()
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n\nTrip stopped by user.")
        
    print("Capturing final data...")
    tracker.end_ts = time.time()
    tracker.end_odometer = tracker.client.read_odometer()
    
    print("Generating report...\n")
    report = tracker.build_report()
    
    print_report(report)
    save_report_json(report, filepath="trip_report.json" if not tracker.start_ts else "trip_report.json")

if __name__ == "__main__":
    main()
