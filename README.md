# youtube-video-scraper

Tools for scraping YouTube video metadata from the YouTube Data API v3 given a list of specified channels. The main intent of this tool is to bulk-scrape titles on publically-available video titles for training with a text-generating AI with a tool such as aitextgen.

For scraping only titles, this script can process about 500,000 videos per 24 hours within the rate limits imposed by the API.

## Setup

First, you need to get an API Key for the YouTube Data v3 API. This can be done by creating a project in Google Cloud Platform and adding access to the YouTube Data v3 API. Then, put this key in the `config.yml` under `API_KEY`.

The Python scripts depend on `requests`, `tqdm`, and `pyyaml`. To install:

```sh
pip3 install requests tqdm pyyaml
```

### Config

The `config.yml` file also contains 30 very-popular YouTube channels, manualy sourced from the Top US YouTube Channels via Socialblade to represent the YouTube "voice." The presence of a channel is not necessairly an endorsement of their content: **please do not send a pull request adding or removing channels.**

You can get a channel ID by looking at the URL of a channel page. Channel IDs always begin with `UC`. If not present (i.e. the channel has a custom channel name URL), reloading the channel page will surface the ID.

## Running The Scripts

The main script is `youtube_video_scraper.py`, which takes the channels specified in `config.yml` and gathers the video ID, title, and publish timestamps for all videos in each channel and places it in `output_folder`, with a seperate CSV for each channel.

If you want to train an AI on YouTube Video Titles, you can run `youtube_video_titles.py`, which extracts only the titles from all the CSVs in the `output_folder`, shuffles them to avoid data leakage, and resaves it as a single-column CSV titled `titles.csv`.

## Ethics

This scraper follows the rules and restrictions imposed by the YouTube Data API v3 and does not attempt to circumvent this.

## Notes

- A `youtube_top_channels.py` script is present as an attempt to programmatically get the top YouTube Channels via the `/search` endpoint. However, after testing, the data returned by YouTube is blatantly wrong. Therefore, the script here is kept for posterity in case YouTube ever fixes that endpoint.

## Maintainer/Creator

Max Woolf ([@minimaxir](https://minimaxir.com))

_Max's open-source projects are supported by his [Patreon](https://www.patreon.com/minimaxir) and [GitHub Sponsors](https://github.com/sponsors/minimaxir). If you found this project helpful, any monetary contributions to the Patreon are appreciated and will be put to good creative use._

## License

MIT
