from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Server is running."

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    if not data or 'youtube_url' not in data:
        return jsonify({"error": "Missing youtube_url"}), 400

    youtube_url = data['youtube_url']
    output_filename = "video.mp4"
    trimmed_filename = "trimmed.mp4"

    try:
        # ✅ Download video using yt-dlp and cookies
        subprocess.run([
            "yt-dlp",
            "--cookies", "cookies.txt",
            "-o", output_filename,
            youtube_url
        ], check=True)

        # ✅ Trim first 60 seconds using ffmpeg
        subprocess.run([
            "ffmpeg", "-y",
            "-i", output_filename,
            "-ss", "00:00:00",
            "-t", "00:01:00",
            "-c:v", "libx264",
            "-c:a", "aac",
            trimmed_filename
        ], check=True)

        return jsonify({
            "message": "✅ Video downloaded and trimmed successfully.",
            "original_url": youtube_url,
            "output_file": trimmed_filename
        })

    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "❌ Download or trim failed.",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
