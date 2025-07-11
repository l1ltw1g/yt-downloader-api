from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    if not data or 'youtube_url' not in data:
        return jsonify({"error": "Missing youtube_url"}), 400

    youtube_url = data['youtube_url']
    print(f"✅ Received YouTube URL: {youtube_url}")

    return jsonify({
        "message": "Server received the URL successfully.",
        "received_url": youtube_url
    })
