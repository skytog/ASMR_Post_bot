#!/usr/bin/env python
# coding: utf-8

import os
from os.path import join, dirname
from dotenv import load_dotenv
import time
import requests
import pandas as pd

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

API_KEY = os.environ.get("YOUTUBE_DATA_API_KEY")

def save_to_csv(videos, filename):
    videos.iloc[:,1] = "https://www.youtube.com/watch?v=" + videos.iloc[:,1]
    videos_asmr = videos[videos["title"].str.contains("ASMR")]
    videos_asmr.to_csv(f'videos_asmr_{filename}.csv', index=None)
    videos.to_csv(f'videos_{filename}.csv', index=None)

def get_video_info(count):
    channel_list = pd.read_csv("Channel_List.csv")
    channel_id = channel_list.iloc[count,1]
    time.sleep(10)
    url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&order=date&maxResults=5'
    response = requests.get(url)
    if response.status_code != 200:
        print('error')
        return
    result = response.json()
    infos = [
        [item['snippet']['title'],  item['id']['videoId'],  item['snippet']['publishedAt'],  item['snippet']['liveBroadcastContent']]
        for item in result['items'] if item['id']['kind'] == 'youtube#video'
    ]
    # Convert the list of video information to a DataFrame
    videos = pd.DataFrame(infos, columns=['title', 'videoId', 'publishedAt', 'liveBroadcastContent'])

    # Save the DataFrame to a CSV file
    save_to_csv(videos, count)
