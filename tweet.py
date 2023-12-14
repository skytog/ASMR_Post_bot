#!/usr/bin/env python
# coding: utf-8

import os
from os.path import join, dirname
from dotenv import load_dotenv
import tweepy
import pandas as pd
from twitter_text import parse_tweet

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")
access_token = os.environ.get("access_token")
access_token_secret = os.environ.get("access_token_secret")
bearer_token = os.environ.get("bearer_token")

def adjust_tweet_length(video_title, tweet_text):
    reduce_count = 0
    judge = parse_tweet(tweet_text).valid
    while not judge:
        reduce_count += 1
        reduce_video_title_len = len(video_title) - reduce_count
        video_title = video_title[:reduce_video_title_len]
        tweet_text = tweet_text.rsplit(video_title, 1)[0] + video_title + "..."
        judge = parse_tweet(tweet_text).valid
    return tweet_text

def create_contents(count):
    client = tweepy.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

    channel_list = pd.read_csv("Channel_List.csv")
    channel_name = channel_list.iloc[count,0]

    video_info = pd.read_csv(f'videos_asmr_{count}.csv')
    video_title = video_info.iloc[0,0]
    video_url = video_info.iloc[0,1]
    video_kinds = video_info.iloc[0,3]

    if video_kinds == "none":
        tweet_text = f"#ASMR #ASMR_fun\n投稿者：{channel_name}\n動画タイトル：{video_title}\n動画URL： {video_url}"
        tweet_text = adjust_tweet_length(video_title, tweet_text)
        client.create_tweet(text=tweet_text)
    elif video_kinds == "upcoming":
        tweet_text = f"#ASMR #ASMR_fun\nライブ予約\n投稿者:{channel_name}\n動画タイトル:{video_title}\n動画URL: {video_url}"
        tweet_text = adjust_tweet_length(video_title, tweet_text)
        client.create_tweet(text=tweet_text)
    else:
        tweet_text = f"#ASMR #ASMR_fun\nライブ中\n投稿者:{channel_name}\n動画タイトル:{video_title}\n動画URL: {video_url}"
        tweet_text = adjust_tweet_length(video_title, tweet_text)
        client.create_tweet(text=tweet_text)
        
    print("tweet complete")
    return