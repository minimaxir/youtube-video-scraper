import yaml
import csv
import os
from tqdm import tqdm
import requests


def process_video(video_snippet):
    temp_dict = {}
    temp_dict["video_id"] = video_snippet["resourceId"]["videoId"]
    temp_dict["title"] = video_snippet["title"]
    temp_dict["video_published_at"] = video_snippet["publishedAt"]
    return temp_dict


with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

API_KEY = config["API_KEY"]
API_URL = "https://www.googleapis.com/youtube/v3/playlistItems"
OUTPUT_FOLDER = config["output_folder"]
OUTPUT_FIELDS = ["video_id", "title", "video_published_at"]
uploads_ids = config["uploads_ids"]

params = {
    "key": API_KEY,
    "part": "snippet",
    "maxResults": 50,
}

for uploads_id in uploads_ids:
    params.update({"playlistId": uploads_id})
    r = requests.get(
        API_URL,
        params=params,
    ).json()
    channel_name = r["items"][0]["snippet"]["channelTitle"]
    pageToken = r.get("nextPageToken")
    pbar = tqdm(total=r["pageInfo"]["totalResults"])
    print(f"Scraping {channel_name}'s videos:")
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
            params.update({"pageToken": pageToken})
            r = requests.get(
                API_URL,
                params=params,
            ).json()
            for video in r["items"]:
                w.writerow(process_video(video["snippet"]))
            pbar.update(len(r["items"]))
            pageToken = r.get("nextPageToken")
    pbar.close()
