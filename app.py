import os
from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/stream')
def stream():
    video_id = request.args.get('videoId')
    if not video_id:
        return jsonify({'error': 'Missing videoId'}), 400

    video_url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info.get('url')
            if not audio_url:
                return jsonify({'error': 'Could not extract audio URL'}), 500
            return jsonify({'streamUrl': audio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Render sets the PORT env variable automatically
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)