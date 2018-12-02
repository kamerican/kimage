from pathlib import Path
from kimage.downloader import Downloader

downloader = Downloader()
urls = Path('urls.txt')
with urls.open(mode='r', newline='') as f:
    url_list = f.readlines()
# print(url_list)
downloader.download_from_list_of_urls(url_list)
