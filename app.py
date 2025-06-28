from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re

app = Flask(__name__)

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

@app.route("/", methods=["POST"])
def get_transcript():
    try:
        data = request.get_json()
        video_url = data.get("youtube_url", "")
        video_id = extract_video_id(video_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["ja", "en"])
        full_text = "\n".join([entry["text"] for entry in transcript])
        return jsonify({"transcript": full_text})
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled"}), 403
    except NoTranscriptFound:
        return jsonify({"error": "No transcript available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
