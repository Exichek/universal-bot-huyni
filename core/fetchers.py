import random
import requests

def search_parrot_short(youtube_api_key):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': 'parrot shorts',
        'type': 'video',
        'videoDuration': 'short',
        'maxResults': 10,
        'key': youtube_api_key
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    items = data.get('items', [])
    if not items:
        return None
    video = random.choice(items)
    video_id = video['id']['videoId']
    return f"https://youtube.com/shorts/{video_id}"

def fetch_currency_rates():
    response = requests.get("https://open.er-api.com/v6/latest", timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_random_article():
    response = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary", timeout=10)
    response.raise_for_status()
    return response.json()
