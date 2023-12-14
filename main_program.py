#!/usr/bin/env python
# coding: utf-8

import time
import pandas as pd
import os
import glob

import get_new_video as gnv
import judgment_time as jt
import tweet

def main():
    """
    This script retrieves video information from a channel list, calculates the time difference between the current time and the last video upload time,
    and tweets about new videos if the time difference is below a certain threshold.
    """

    for file in glob.glob('videos_*.csv'):
        os.remove(file)

    Ch_list = pd.read_csv("Channel_List.csv", header=1)
    Ch_col = len(Ch_list)
    threshold = 72000

    for count in range(1, Ch_col +1):
        print(str(count) + "回目")
        gnv.get_video_info(count)
        try:
            time_difference = jt.calculate_time_difference(count)
        except IndexError:
            print("No Timedata")
            continue

        if threshold > time_difference:
            print(time_difference)
            print("new video found")
            tweet.create_contents(count)
        else:
            print("not found")

if __name__ == "__main__":
    main()


