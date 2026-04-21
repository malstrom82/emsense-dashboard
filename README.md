# Radar Sensor Dashboard (MVP)

This project is a prototype dashboard for visualizing and interacting with synthetic radar-based physiological data (e.g., heart rate) collected from multiple vehicles.

The system simulates:

* Multiple cars deployed globally
* Active vs inactive sensor states
* Heart rate signals with noise and artifacts
* Reliability metrics for signal quality

The dashboard allows you to:

* View currently active vehicles (Home page)
* Explore the full fleet with aggregated statistics (Fleet page)
* Inspect individual vehicles with detailed signal graphs and metrics
* See approximate global distribution of vehicles (Map page)
* Observe simulated “live” updates for active vehicles

---

## Setup & Run Instructions

### 1. Generate synthetic dataset

From the project root folder:

```
python src\generate_data.py
```

This will create:

```
data\synthetic_data.csv
```

---

### 2. Start the dashboard app

```
cd app
python app.py
```

---

### 3. Open in browser

Copy the address shown in the terminal (typically):

```
http://127.0.0.1:8050/
```

Paste it into your web browser to access the dashboard.

---

## Notes

* If you modify code, stop the app with `Ctrl + C` and restart it
* Active vehicles will show simulated live updates
* Inactive vehicles display static data

---

## Status

This is a **minimum viable prototype (MVP)** using synthetic data for demonstration purposes.
Further development may include real data integration, advanced reliability analysis, and improved geospatial accuracy.
