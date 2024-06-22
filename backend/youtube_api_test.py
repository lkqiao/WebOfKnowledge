import datetime

import isodate
import requests

from backend.dislikes import get_dislike_count

# Your API key
API_KEY = 'AIzaSyBuEW6_VrihFewcGlGk44rwaa0CRaw8qMs'




def search_videos(query):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    search_params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 40,  # Number of results to return
        'key': API_KEY
    }
    response = requests.get(search_url, params=search_params)
    return response.json() if response.status_code == 200 else None


def get_video_details(video_id):
    video_url = 'https://www.googleapis.com/youtube/v3/videos'
    video_params = {
        'part': 'snippet,contentDetails,statistics',
        'id': video_id,
        'key': API_KEY
    }
    response = requests.get(video_url, params=video_params)
    return response.json() if response.status_code == 200 else None


def fetch_videos_info(search_query):
    search_results = search_videos(search_query)
    if search_results and 'items' in search_results:
        videos_info = []
        for item in search_results['items']:
            video_id = item['id']['videoId']
            video_details = get_video_details(video_id)
            if video_details and 'items' in video_details:
                video = video_details['items'][0]
                video_info = {
                    "Title": video['snippet']['title'],
                    "Video ID": video_id,
                    "Channel": video['snippet']['channelTitle'],
                    "Published at": datetime.datetime.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                    "View Count": video['statistics'].get('viewCount', 'N/A'),
                    "Like Count": video['statistics'].get('likeCount', 'N/A'),
                    "Comment Count": video['statistics'].get('commentCount', 'N/A'),
                    "Duration": isodate.parse_duration(video['contentDetails']['duration']).total_seconds(),
                    "Dislike Count": get_dislike_count(video_id)
                }
                videos_info.append(video_info)
                # add a section for scores
                video_info["Scores"] = {}

                # if like count is not available, set it to 0
                if video_info["Like Count"] != "N/A":
                    # add like to dislike ratio
                    video_info["Scores"]["Like to Dislike Ratio"] = float(video_info["Like Count"]) / (int(
                        video_info["Dislike Count"]) + 1)

                    # add like to view ratio
                    video_info["Scores"]["Like to View Ratio"] = float(video_info["Like Count"]) / (int(
                        video_info["View Count"]) + 1)

                # add comment to view ratio
                video_info["Scores"]["Comment to View Ratio"] = float(video_info["Comment Count"]) / (int(
                    video_info["View Count"]) + 1)

                # add recency score
                video_info["Scores"]["Recency Score"] = (datetime.datetime.now() - video_info["Published at"]).days

        return videos_info
    else:
        return {"error": "No results found or there was an error with the search."}


if __name__ == "__main__":
    SEARCH_QUERY = 'Python programming'
    videos_info = fetch_videos_info(SEARCH_QUERY)
    print(videos_info)

    # get an array of just like to dislike ratios (if available)
    like_to_dislike_ratios = [video["Scores"]["Like to Dislike Ratio"] for video in videos_info if
                              "Like to Dislike Ratio" in video["Scores"]]

    # get an array of just like to view ratios (if available)
    like_to_view_ratios = [video["Scores"]["Like to View Ratio"] for video in videos_info if
                           "Like to View Ratio" in video["Scores"]]

    # get an array of just comment to view ratios (if available)
    comment_to_view_ratios = [video["Scores"]["Comment to View Ratio"] for video in videos_info if
                              "Comment to View Ratio" in video["Scores"]]

    # get an array of just recency scores (if available)
    recency_scores = [video["Scores"]["Recency Score"] for video in videos_info if "Recency Score" in video["Scores"]]

    print(f"Like to Dislike Ratios: {like_to_dislike_ratios}")
    print(f"Like to View Ratios: {like_to_view_ratios}")
    print(f"Comment to View Ratios: {comment_to_view_ratios}")
    print(f"Recency Scores: {recency_scores}")

    import matplotlib.pyplot as plt

    # Create a figure with 4 subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Metrics for YouTube Videos')

    # Flatten the axs array for easier indexing
    axs = axs.flatten()

    # Create dot plots for each metric
    metrics = [
        (like_to_dislike_ratios, 'Like to Dislike Ratio', 'r'),
        (like_to_view_ratios, 'Like to View Ratio', 'b'),
        (comment_to_view_ratios, 'Comment to View Ratio', 'g'),
        (recency_scores, 'Recency Score', 'y')
    ]

    for i, (data, title, color) in enumerate(metrics):
        # Create a one-dimensional dot plot
        axs[i].plot(data, [0] * len(data), 'o', color=color)
        axs[i].set_title(title)

        # Remove y-axis ticks
        axs[i].yaxis.set_ticks([])

        # Add a horizontal line at y=0
        axs[i].axhline(y=0, color='k', linestyle='-', linewidth=0.5)

        # Set y-axis limits to create some padding
        axs[i].set_ylim(-0.5, 0.5)

        # Adjust x-axis limits to add some padding
        x_min, x_max = min(data), max(data)
        x_range = x_max - x_min
        axs[i].set_xlim(x_min - 0.05 * x_range, x_max + 0.05 * x_range)

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()



