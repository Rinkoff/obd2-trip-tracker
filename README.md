# OBD2 Data Tracker

A professional CLI application designed for real-time collection, processing, and analysis of vehicle telemetry data via the OBD-II interface (ELM327).
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📋 Overview

The OBD2 Data Tracker allows for seamless trip monitoring by connecting to an OBD-II adapter. It automatically calculates fuel consumption, distance traveled, and identifies potential driving behavior issues (e.g., excessive idling or aggressive acceleration), providing actionable insights from raw vehicle data.

## ✨ Key Features

-   **Real-time Telemetry:** Synchronous polling of RPM, Speed, Throttle Position, Engine Load, and Mass Air Flow (MAF).
-   **Advanced Analytics:** 
    -   **Fuel Estimation:** Accurate fuel consumption tracking using MAF-based physics integration.
    -   **Distance Logic:** Smart distance calculation with fallback integration (integrating speed over time if odometer data is unavailable).
-   **Driving Behavior Intelligence:** An analysis layer that detects:
    -   Hardware-level performance anomalies.
    -   Frequent hard acceleration (aggressive driving).
    -   High RPM at low speeds.
    -   Excessive idling (Long Idle detection).
-   **Structured Reporting:** Generates detailed JSON reports and console summaries post-trip for data persistence and review.
-   **Hardware Mocking:** Full support for `MockClient`, enabling development and integration testing without requiring physical vehicle access.

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/obd2-data-tracker.git
   cd obd2-data-tracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run in simulation mode:**
   ```bash
   python obd2_trip_tracker.py --simulate
   ```

## 📈 Roadmap

-   [ ] **Web Dashboard:** Integrate Flask/Streamlit for advanced data visualization and charts.
-   [ ] **Persistence Layer:** Add SQLite support for historical trip comparison.
-   [ ] **GPS Integration:** Map routes by correlating OBD data with GPS coordinates.

---
*Developed as a technical showcase for IoT and Python systems programming.*
