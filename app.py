from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os

app = Flask(__name__)

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    data = request.json
    
    if not data or 'videoId' not in data:
        return jsonify({'error': 'videoId requis'}), 400
    
    video_id = data['videoId']
    
    try:
        # Tenter de récupérer la transcription
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr', 'en'])
        
        # Formatter la transcription en texte simple
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript_list)
        
        return jsonify({
            'success': True,
            'videoId': video_id,
            'transcript': transcript_text
        })
    
    except Exception as e:
        # Gérer les erreurs (transcription non disponible, etc.)
        return jsonify({
            'success': False,
            'videoId': video_id,
            'error': str(e)
        }), 404

# Ajouter un endpoint de santé pour vérifier que le service fonctionne
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

# Ajouter CORS headers pour éviter les problèmes avec n8n
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
