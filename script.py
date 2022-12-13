import json
import os
import sys

from pathlib import Path

from pytube import YouTube
from tqdm import tqdm


def download():
    with open("wanted_musics.json") as file:
        data = json.load(file)
        already_downloaded = data["already_downloaded"]
        to_download = data["to_download"]
    
    initial_urls_number = len(to_download)

    if not to_download:
        print("Nothing to download ...\n")
        exit()

    count = 0
    not_downloaded = []
    
    while tqdm(to_download):
        for url in to_download:
            if url in already_downloaded:
                print(f"{url} is already downloaded.\n")
                continue

            yt = YouTube(url)

            ##@ Extract audio with 160kbps quality from video
            video = yt.streams.filter(abr='160kbps').last()

            ##@ Downloadthe file
            out_file = video.download(output_path="music_mp3")
            base, ext = os.path.splitext(out_file)
            new_file = Path(f'{base}.mp3')
            os.rename(out_file, new_file)
            ##@ Check success of download
            if new_file.exists():
                count += 1
            else:
                not_downloaded.append(yt.title)

            to_download.remove(url)
            already_downloaded.append(url)

        with open("wanted_musics.json", "w") as out:
            json.dump(
            {
                "to_download": to_download,
                "already_downloaded": already_downloaded
            }, out, indent=4)

    print(f"\n{count}/{initial_urls_number} musics successfully downloaded.\n")

    if not_downloaded:
        n = '\n'
        print(f"{len(not_downloaded)} music(s) were not downloaded:\n{n.join(not_downloaded)}\n")

def add_link(url):
    with open("wanted_musics.json", "r+") as file:

        data = json.load(file)
        
        if url in data["to_download"]:
            print("\nURL already in list\n")
            return
        
        data["to_download"].append(url)

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    
    print("\nLink added\n")


if len(sys.argv) < 2:
    print("Please specify an argument.\n\n-d to download the current list\n\n-add [link]")

if sys.argv[1] == "-d":
    download()

if sys.argv[1] == "-add":
    add_link(sys.argv[2])
