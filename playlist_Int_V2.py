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

# Function to download the playlist with accurate video titles
def download_youtube_playlist(playlist_url, save_location):
    playlist = Playlist(playlist_url)
    for video in playlist.videos:
        video_id = video.video_id
        title = get_video_title(video_id)
        filename = os.path.join(save_location, title + ".mp4")  # Save file as .mp4
        
        stream_1080p = video.streams.filter(res="1080p").first()
        stream_720p = video.streams.filter(res="720p").first()
        
        if stream_1080p:
            stream = stream_1080p
        elif stream_720p:
            stream = stream_720p
        else:
            stream = video.streams.first()  # Get the best available quality
        
        if stream:
            if not os.path.exists(filename):
                stream.download(output_path=save_location, filename=title + ".mp4")  # Save with the correct filename and location
                print(f"Downloaded: {title}")
            else:
                print(f"Skipped: {title} - Already downloaded")
        else:
            print(f"No suitable streams found for: {title}")

# Prompt user for YouTube playlist URL and download location
playlist_url = input("Enter the YouTube playlist URL: ")
save_location = input("Enter the location to save downloads: ")

# Call the function with the playlist URL and download location
download_youtube_playlist(playlist_url, save_location)