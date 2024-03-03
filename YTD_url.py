import os
import requests

# Function to download a file from a URL
def download_file_from_url(url, save_location):
    filename = os.path.join(save_location, url.split("/")[-1])  # Extract filename from URL
    if os.path.exists(filename):
        print(f"Skipped: {filename} - Already exists")
        return
    
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

# Prompt user for URL and download location
url = input("Enter the URL of the file to download: ")
save_location = input("Enter the location to save the file: ")

# Call the function to download the file
download_file_from_url(url, save_location)
