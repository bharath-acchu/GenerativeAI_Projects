from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(youtube_url):
    try:
        # Extract video ID
        video_id = youtube_url.split("v=")[-1].split("&")[0]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine into one big text
        text = " ".join([entry['text'] for entry in transcript])
        return text
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None
