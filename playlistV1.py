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
def download_youtube_playlist(playlist_url):
    playlist = Playlist(playlist_url)
    for video in playlist.videos:
        video_id = video.video_id
        title = get_video_title(video_id)
        filename = title + ".mp4"
        
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
                stream.download(filename=title)
                print(f"Downloaded: {title}")
            else:
                print(f"Skipped: {title} - Already downloaded")
        else:
            print(f"No suitable streams found for: {title}")

# Provide the URL of the YouTube playlist you want to download
playlist_url = "https://www.youtube.com/playlist?list=PL-71OxJ8uG1yqhQjOE-YQYhRNaYb_pzcx"

# Call the function with the playlist URL
download_youtube_playlist(playlist_url)