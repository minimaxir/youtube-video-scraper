import yaml
import csv
import os
from random import shuffle

with open("config.yml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

OUTPUT_FOLDER = config["output_folder"]

files = os.listdir(OUTPUT_FOLDER)
titles = []

for file in files:
    with open(os.path.join(OUTPUT_FOLDER, file), "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            titles.append(row["title"])

shuffle(titles)

with open("titles.csv", "w", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["title"])
    for title in titles:
        w.writerow([title])
