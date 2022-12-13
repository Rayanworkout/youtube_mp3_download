import json
import os
import re
import sys

from pathlib import Path

from pytube import YouTube

print()

if not os.path.isdir("data"):
    os.mkdir("data")

if not os.path.exists("urls.json"):
    with open("urls.json", "w") as file:
        json.dump({"to_download": [],
                    "already_downloaded": []}
                    )

def download(verbose=False):
    with open("urls.json") as file:
        data = json.load(file)
        already_downloaded = data["already_downloaded"]
        to_download = data["to_download"]
    
    initial_urls_number = len(to_download)

    if not to_download:
        print("Nothing to download ...\n")
        exit()
    
    if verbose:
        print(f"{initial_urls_number} URLS to download.")

    count = 0
    not_downloaded = []
    
    while to_download:
        for url in to_download:
            if url in already_downloaded:
                print(f"{url} is already downloaded.\n")
                continue

            yt = YouTube(url)

            # Extract audio with 160kbps quality from video
            video = yt.streams.filter(abr='160kbps').last()

            # Downloadthe file
            out_file = video.download(output_path="data")
            base, ext = os.path.splitext(out_file)
            new_file = Path(f'{base}.mp3')
            os.rename(out_file, new_file)

            # Check success of download
            if new_file.exists():
                count += 1
            else:
                not_downloaded.append(yt.title)

            to_download.remove(url)
            already_downloaded.append(url)
        
            if verbose:
                print(f"Successfully downloaded {yt.title}")
                print("...")


        with open("urls.json", "w") as out:
            json.dump(
            {
                "to_download": to_download,
                "already_downloaded": already_downloaded
            }, out, indent=4)
        
        if verbose:
            print("List updated.")
            print("...")

    print(f"\n{count}/{initial_urls_number} URLS successfully downloaded.\n")

    if not_downloaded:
        n = '\n'
        print(f"{len(not_downloaded)} URL(S) were not downloaded:\n{n.join(not_downloaded)}\n")



def add_link(url):
    if not re.match(r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$', url):
        print("This is not a valid youtube URL, try again")
        return

    with open("urls.json", "r+") as file:

        data = json.load(file)
        
        if url in data["to_download"]:
            print("URL already in list\n")
            return
        
        data["to_download"].append(url)

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()
    
    print("Link added\n")


equals = f"{40 * '='}"

if len(sys.argv) == 1:
    print(equals)
    print("    Please specify an argument")
    print(equals)
    print("\n-d to download the current list\n\n-add [link] to add a new link to the list\n\n-v can be added with -d argument\n")

elif len(sys.argv) > 3:
    print(equals)
    print("    Too much arguments")
    print(equals)
    print("\n-d to download the current list\n\n-add [link] to add a new link to the list\n\n-v can be added with -d argument\n")

elif len(sys.argv) > 1 and sys.argv[1] not in ["-d", "-add"]:
    print(equals)
    print("    Wrong argument. Please specify the correct one")
    print(equals)
    print("\n-d to download the current list\n\n-add [link] to add a new link to the list\n\n-v can be added with -d argument\n")

elif len(sys.argv) == 2 and sys.argv[1] == "-add":
    print(equals)
    print("    You need to specify an URL with the -add argument.\n")
    print(equals)


elif sys.argv[1] == "-add":
    add_link(sys.argv[2])

elif len(sys.argv) == 3 and sys.argv[1] == "-d" and sys.argv[2] == "-v":
    download(verbose=True)

elif sys.argv[1] == "-d":
    download()
