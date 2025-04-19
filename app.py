from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
import os

app = Flask(__name__)

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    data = request.json
    
    if not data or 'videoId' not in data:
        return jsonify({'success': False, 'error': 'videoId requis'}), 400
    
    video_id = data['videoId']
    
    try:
        # Tenter de récupérer la transcription avec plusieurs langues possibles
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['fr', 'en', 'es', 'de', 'auto'])
        
        # Convertir la liste de segments en texte continu
        transcript_text = ' '.join([segment['text'] for segment in transcript_list])
        
        return jsonify({
            'success': True,
            'videoId': video_id,
            'transcript': transcript_text
        })
    
    except NoTranscriptFound:
        return jsonify({
            'success': False,
            'videoId': video_id,
            'error': "Aucune transcription trouvée pour les langues demandées."
        }), 404
    
    except TranscriptsDisabled:
        return jsonify({
            'success': False,
            'videoId': video_id,
            'error': "Les transcriptions sont désactivées pour cette vidéo."
        }), 404
    
    except VideoUnavailable:
        return jsonify({
            'success': False,
            'videoId': video_id,
            'error': "La vidéo n'est pas disponible ou n'existe pas."
        }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'videoId': video_id,
            'error': f"Erreur lors de la récupération de la transcription: {str(e)}"
        }), 500

# Ajouter un endpoint de santé
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

# Ajouter CORS headers
@app.after_request
def add_cors_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
