import glob
import os
from mutagen.mp4 import MP4, MP4Cover
def process_nwn2_scripts():
    preprocessing_folder = "./Spotify_PreProcessing_Local_Music_Folder"
    format_main(preprocessing_folder)
    format_motb(preprocessing_folder)
    format_storm(preprocessing_folder)


def format_album(files_in_album, split_deliminator,album_image_path,album_name,contributing_artists):
    files = glob.glob(files_in_album)
    for id,file in enumerate(files):
        file_info = file.split(split_deliminator)
        if file_info:
            title = file_info[1][:-4]
            new_file_name = f"{id}. {title}.mp4"
            song_mp4 = MP4(file)
            song_mp4["\xa9nam"] = title
            song_mp4["\xa9alb"] = album_name
            song_mp4["\xa9ART"] = contributing_artists

            with open(album_image_path, "rb") as f:
                song_mp4.tags["covr"] = [
                    MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
                ]

            song_mp4.save()
            os.rename(file,new_file_name)

def format_main(preprocessing_folder_path: str):
    main_files = f"{preprocessing_folder_path}/NWN2_MAIN/*.mp4"
    album_name = "Neverwinter Nights 2 Official Soundtrack"
    album_image_path = f"{preprocessing_folder_path}/NWN2_MAIN/album_cover.jpg"
    contributing_artists = "Neil Goldberg & Dave G. Fraser"
    format_album(main_files," - ",album_image_path,album_name,contributing_artists)

def format_motb(preprocessing_folder_path: str):
    main_files = f"{preprocessing_folder_path}/NWN2_MOTB/*.mp4"
    album_name = "Neverwinter Nights 2 Official Soundtrack - Mask of the Betrayer"
    album_image_path = f"{preprocessing_folder_path}/NWN2_MOTB/album_cover.jpg"
    contributing_artists = "Rik Shaffer"
    format_album(main_files," - ",album_image_path,album_name,contributing_artists)

def format_storm(preprocessing_folder_path: str):
    main_files = f"{preprocessing_folder_path}/NWN2_SOZ/*.mp4"
    album_name = "Neverwinter Nights 2 Official Soundtrack - Storm of Zehir"
    album_image_path = f"{preprocessing_folder_path}/NWN2_SOZ/album_cover.jpg"
    contributing_artists = "Andrew Barnabas & Paul Arnold"
    format_album(main_files,"Soundtrack ",album_image_path,album_name,contributing_artists)

if __name__ == "__main__":
    process_nwn2_scripts()