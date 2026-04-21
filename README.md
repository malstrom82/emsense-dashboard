# Radar Sensor Dashboard (MVP)

This project is an interactive dashboard for visualizing synthetic radar-based physiological data (e.g., heart rate) collected from multiple vehicles.

The system simulates:

* A fleet of vehicles distributed globally
* Active vs inactive sensor states
* Heart rate signals with noise, artifacts, and dropouts
* Reliability metrics for signal quality

---

## Features

* **Home page**: Displays currently active vehicles
* **Fleet page**: Overview of all vehicles with aggregated statistics
* **Car detail pages**: Signal visualization and per-car diagnostics
* **Map view**: Approximate global distribution of vehicles
* **Live simulation**: Active vehicles show continuously updating signals

---

## Local Setup & Run

### 1. Generate synthetic dataset

From the project root:

```bash
python src\generate_data.py
```

This creates:

```text
data/synthetic_data.csv
```

---

### 2. Start the dashboard

```bash
python app\app.py
```

---

### 3. Open in browser

Copy the address shown in the terminal:

```text
http://127.0.0.1:8050/
```

Paste it into your web browser.

---

### Notes

* Stop the app with `Ctrl + C` in terminal
* Restart after code changes
* Active vehicles simulate live updates
* Inactive vehicles show static data

---

## Status

This is a **minimum viable prototype (MVP)** using synthetic data.

Future improvements may include:

* Real sensor integration
* Improved geolocation (lat/lon)
* Reliability-based anomaly detection
* Persistent backend storage

---
