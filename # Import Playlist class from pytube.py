# Import Playlist class from pytube
from pytube import Playlist
import os
import requests

# Function to fetch video title using YouTube Data API
def get_video_title(video_id):
    api_key = "AIzaSyCyvuGPfu4W5rKMwctn4b9kIaQWwg1cwHU"
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet"
    response = requests.get(url)
    data = response.json()
    
    try:
        title = data["items"][0]["snippet"]["title"]
        return title
    except KeyError:
        print("Error: Unable to retrieve video title")
        return "Unknown Title"

# Function to download the playlist with accurate video titles starting from the newest
def download_youtube_playlist(playlist_url, save_location):
    downloaded_count = 0
    skipped_count = 0
    
    supported_codecs = ["H.264", "DV", "Motion JPEG A", "Motion JPEG B", "MPEG-4"]
    
    playlist = Playlist(playlist_url)
    
    for video in reversed(playlist.videos):
        video_id = video.video_id
        title = get_video_title(video_id)
        filename = os.path.join(save_location, title + ".mp4")  # Save file as .mp4
        
        if os.path.exists(filename):
            print(f"Skipped: {title} - Already exists")
            skipped_count += 1
            continue
        
        stream = None
        for codec in supported_codecs:
            stream = video.streams.filter(file_extension='mp4', res="1080p", video_codec=codec).first()
            if stream:
                break
        
        if stream:
            print(f"\nVideo Title: {title}")
            choice = input("Do you want to download this video? (y/n): ")
            
            if choice.lower() == 'y':
                stream.download(output_path=save_location, filename=title + ".mp4")  # Save with the correct filename and location
                print(f"Downloaded: {title}")
                downloaded_count += 1
            else:
                print(f"Skipped: {title}")
                skipped_count += 1
        else:
            print(f"No suitable streams found for: {title}")
    
    # Summary report
    print("\nDownload Summary:")
    print(f"Total Videos Downloaded: {downloaded_count}")
    print(f"Total Videos Skipped: {skipped_count}")

# Prompt user for YouTube playlist URL and download location
playlist_url = input("Enter the YouTube playlist URL: ")
save_location = input("Enter the location to save downloads: ")

# Call the function with the playlist URL and download location
download_youtube_playlist(playlist_url, save_location)
