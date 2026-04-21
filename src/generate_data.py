# src/generate_data.py

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

FREQ = 10  # Hz


# =========================
# CAR CONFIG
# =========================
CARS = [
    ("car_1", "Sweden", "Gothenburg"),
    ("car_2", "Germany", "Munich"),
    ("car_3", "France", "Paris"),
    ("car_4", "USA", "San Francisco"),
    ("car_5", "USA", "New York"),
    ("car_6", "Japan", "Tokyo"),
    ("car_7", "South Korea", "Seoul"),
    ("car_8", "Spain", "Barcelona"),
    ("car_9", "Italy", "Rome"),
    ("car_10", "UK", "London"),
]

ACTIVE_CARS = {"car_1", "car_6", "car_7"}  # force active


# =========================
# DATA GENERATION
# =========================
def generate_car_data(car_id, country, city, duration_sec=300):
    n = duration_sec * FREQ
    t = np.linspace(0, duration_sec, n)

    base_hr = np.random.uniform(60, 85)

    hr = base_hr + 5 * np.sin(0.1 * t)
    noise = np.random.normal(0, 2, n)

    motion = np.random.rand(n) < 0.01
    hr[motion] += np.random.normal(20, 5, motion.sum())

    dropout = np.random.rand(n) < 0.005
    hr[dropout] = np.nan

    quality = np.clip(
        1 - (np.abs(noise)/5 + motion*0.5 + dropout*0.7),
        0, 1
    )

    # =========================
    # ACTIVITY
    # =========================
    activity = np.zeros(n, dtype=bool)

    if car_id in ACTIVE_CARS:
        # last part active (simulate currently running)
        activity[-int(n * 0.3):] = True
    else:
        # historical sessions only
        for _ in range(3):
            start = np.random.randint(0, n - 200)
            activity[start:start+100] = True

    start_time = datetime.now()
    timestamps = [start_time + timedelta(seconds=i/FREQ) for i in range(n)]

    return pd.DataFrame({
        "timestamp": timestamps,
        "car_id": car_id,
        "country": country,
        "city": city,
        "heart_rate": hr + noise,
        "signal_quality": quality,
        "motion_artifact": motion,
        "dropout": dropout,
        "is_active": activity
    })


# =========================
# RELIABILITY
# =========================
def compute_reliability(df):
    df = df.copy()

    df["hr_diff"] = df.groupby("car_id")["heart_rate"].diff().abs()
    smoothness = np.exp(-df["hr_diff"].fillna(0) / 10)

    df["reliability"] = (
        0.5 * df["signal_quality"] +
        0.3 * smoothness +
        0.2 * (~df["dropout"]).astype(int)
    )

    return df


# =========================
# PATH
# =========================
def get_data_path():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "synthetic_data.csv")


# =========================
# MAIN
# =========================
def main():
    df_list = [generate_car_data(*car) for car in CARS]
    df = pd.concat(df_list).reset_index(drop=True)

    df = compute_reliability(df)

    path = get_data_path()
    df.to_csv(path, index=False)

    print("Saved:", path)
    print("Active cars:", ACTIVE_CARS)


if __name__ == "__main__":
    main()