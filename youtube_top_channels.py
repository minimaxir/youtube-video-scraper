import yaml
from tqdm import tqdm
import requests
import os
import csv


def process_channel(channel_id, channel_snippet, channel_statistics):
    temp_dict = {}
    temp_dict["channel_id"] = channel_id
    temp_dict["title"] = channel_snippet["title"]
    temp_dict["country"] = channel_snippet.get("country", "")
    temp_dict["channel_created_at"] = channel_snippet["publishedAt"]
    temp_dict["view_count"] = channel_statistics["viewCount"]
    temp_dict["subscriber_count"] = channel_statistics.get("subscriberCount", "")
    temp_dict["video_count"] = channel_statistics["videoCount"]
    return temp_dict


with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

MAX_CHANNELS = 10 ** 2
API_KEY = config["API_KEY"]
SEARCH_API_URL = "https://www.googleapis.com/youtube/v3/search"
CHANNEL_API_URL = "https://www.googleapis.com/youtube/v3/channels"
OUTPUT_FOLDER = config["output_folder"]
OUTPUT_FIELDS = [
    "channel_id",
    "title",
    "country",
    "channel_created_at",
    "view_count",
    "subscriber_count",
    "video_count",
]
uploads_ids = config["uploads_ids"]

search_params = {
    "key": API_KEY,
    "type": "channel",
    "order": "viewCount",
    "regionCode": "US",
    "maxResults": 50,
}

channel_params = {
    "key": API_KEY,
    "part": "snippet,statistics",
    "maxResults": 50,
}

count = 0
pbar = tqdm(total=MAX_CHANNELS)

with open(os.path.join(OUTPUT_FOLDER, "top_channels.csv"), "w", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
    w.writeheader()
    while count < MAX_CHANNELS:
        r = requests.get(SEARCH_API_URL, params=search_params).json()
        search_params.update({"pageToken": r.get("nextPageToken")})

        channel_ids = [x["id"]["channelId"] for x in r["items"]]
        channel_params.update({"id": ",".join(channel_ids)})

        r = requests.get(CHANNEL_API_URL, params=channel_params).json()
        for channel in r["items"]:
            w.writerow(
                process_channel(
                    channel["id"], channel["snippet"], channel["statistics"]
                )
            )
        count += len(r["items"])
        pbar.update(len(r["items"]))
    pbar.close()
