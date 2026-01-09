from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/yt")
def yt():
    video_id = request.args.get("v")
    if not video_id:
        return jsonify({"error": "Missing video ID"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "format": "best[ext=mp4]/best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            stream_url = info["url"]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"stream": stream_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
