import yaml
import csv
import os
from tqdm import tqdm
import requests
import time


def process_video(video_snippet):
    temp_dict = {}
    temp_dict["video_id"] = video_snippet["resourceId"]["videoId"]
    temp_dict["title"] = video_snippet["title"]
    temp_dict["video_published_at"] = video_snippet["publishedAt"]
    return temp_dict


with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

API_KEY = config["API_KEY"]
CHANNELS_API_URL = "https://www.googleapis.com/youtube/v3/channels"
PLAYLIST_API_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
OUTPUT_FOLDER = config["output_folder"]
OUTPUT_FIELDS = ["video_id", "title", "video_published_at"]
channel_ids = config["channel_ids"]

channels_params = {
    "key": API_KEY,
    "part": "contentDetails",
}

playlist_params = {
    "key": API_KEY,
    "part": "snippet",
    "maxResults": 50,
}

for channel_id in channel_ids:
    channels_params.update({"id": channel_id})

    r = requests.get(
        CHANNELS_API_URL,
        params=channels_params,
    ).json()

    # the uploads_id indicates the playlist where a channel's uploads are located
    uploads_id = r["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    playlist_params.update({"playlistId": uploads_id})
    r = requests.get(
        PLAYLIST_API_URL,
        params=playlist_params,
    ).json()

    if "items" in r:
        channel_name = r["items"][0]["snippet"]["channelTitle"]
        pageToken = r.get("nextPageToken")
        print(f"Scraping {channel_name}'s videos:")
        pbar = tqdm(total=r["pageInfo"]["totalResults"])
        with open(
            os.path.join(OUTPUT_FOLDER, f"{channel_name}.csv"), "w", encoding="utf-8"
        ) as f:
            w = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
            w.writeheader()

            # process first page we already queried
            for video in r["items"]:
                w.writerow(process_video(video["snippet"]))
            pbar.update(len(r["items"]))

            # process the rest
            while pageToken:
                playlist_params.update({"pageToken": pageToken})
                r = requests.get(
                    PLAYLIST_API_URL,
                    params=playlist_params,
                ).json()
                for video in r["items"]:
                    w.writerow(process_video(video["snippet"]))
                pbar.update(len(r["items"]))
                pageToken = r.get("nextPageToken")
                time.sleep(0.1)
        pbar.close()
        # reset pageToken for new channel
        playlist_params.update({"pageToken": None})
