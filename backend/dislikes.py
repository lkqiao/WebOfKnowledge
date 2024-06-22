import requests
import json


def get_dislike_count(video_id):
    url = f"https://returnyoutubedislikeapi.com/votes?videoId={video_id}"

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        return data.get('dislikes', "Dislike count not found")

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON response"}


if __name__ == "__main__":
    video_id = "kxOuG8jMIgI"
    dislikes = get_dislike_count(video_id)
    print(dislikes)
