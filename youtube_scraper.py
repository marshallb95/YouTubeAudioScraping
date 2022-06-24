import os
import glob
from pytube import YouTube, Playlist
import requests

from typing import Dict

class YouTubeScraper:
    def __init__(self,preprocessing_filepath: str, playlist_urls: Dict[str,str]):
        self.preprocessing_filepath = preprocessing_filepath
        self.playlist_urls = playlist_urls
    def download_audio_playlist(self,album_filepath,playlist_url: str):
        playlist = Playlist(playlist_url)
        for vid_url in playlist:
            vid = YouTube(vid_url)
            streams = vid.streams.filter(file_extension="mp4",only_audio=True)
            for stream in streams:
                stream.download(output_path=album_filepath,skip_existing=True)

    def download_album_cover(self,album_folder_filepath:str, playlist_url: str):
        playlist = Playlist(playlist_url)
        for vid_url in playlist[0:1]:
            vid = YouTube(vid_url)
            thumbnail = vid.thumbnail_url
            #print("thumbnail",thumbnail)
            #replace_jpg_string = "sddefault\.jpg|hqdefault\.jpg"
            #max_res_thumbnail = re.sub(replace_jpg_string,"maxresdefault.jpg",thumbnail)
            #print("subbed thumbnail",thumbnail)
            resp = requests.get(thumbnail)
            if not resp.ok:
                raise ValueError("An Error Occurred fetching the requested image", thumbnail," with status code", resp.status_code)
            img_data = resp.content

            with open(f"{album_folder_filepath}/album_cover.jpg",'wb') as cover_image:
                cover_image.write(img_data)
            
    def create_folders(self):
        for folder_title in self.playlist_urls.keys():
            folder_path = f"{preprocessing_folder_path}/{folder_title}/"
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

    def get_album_covers(self):
        for folder_title,playlist_url in self.playlist_urls.items():
            album_path = f"{self.preprocessing_filepath}/{folder_title}/"
            cover_image = f"{album_path}/album_cover.png"
            if not os.path.exists(cover_image):
                self.download_album_cover(album_path,playlist_url)

    def get_album_songs(self):
        for folder_title,playlist_url in self.playlist_urls.items():
            album_path = f"{self.preprocessing_filepath}/{folder_title}/"
            mp4s = glob.glob(f"{album_path}*.mp4")
            if mp4s:
                continue
            else:
                self.download_audio_playlist(album_path,playlist_url)
            

    def generate_content(self):
        self.create_folders()
        self.get_album_covers()
        self.get_album_songs()

if __name__ == "__main__":
    preprocessing_folder_path = "./Spotify_PreProcessing_Local_Music_Folder"
    nwn2_dict = {"NWN2_MAIN": "https://www.youtube.com/playlist?list=PL3lm7YmWEtOpkIYvtHWrd1hVX9kut0wVp", "NWN2_MOTB": "https://www.youtube.com/playlist?list=PLdeFYxjwVT6HlTbh9zDHi-eQlMPAxittU","NWN2_SOZ": "https://www.youtube.com/playlist?list=PL2B8C78139AA0BB44"}
    yts = YouTubeScraper(preprocessing_folder_path,nwn2_dict)
    yts.generate_content()