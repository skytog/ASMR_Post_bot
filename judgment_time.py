#!/usr/bin/env python
# coding: utf-8

import datetime as dt
import pandas as pd

def calculate_time_difference(count):
    dt_now = dt.datetime.utcnow()

    try:
        df = pd.read_csv(f"videos_asmr_{count}.csv")
        dt_pub_str = df.iloc[0, 2]
    except (FileNotFoundError, pd.errors.EmptyDataError, IndexError):
        print("No Timedata")
        return 72001

    dt_pub = dt.datetime.strptime(dt_pub_str.replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
    time_difference = (dt_now - dt_pub).total_seconds()

    print(f"現在時刻との差は{time_difference}")
    return time_difference