from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models.detector import BullyingDetector
from config.settings import Config
import logging.config
import pytesseract
import datetime
import base64
import io
from PIL import Image
import traceback

# Configure logging
logging.config.dictConfig(Config.LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Update CORS configuration for mobile access
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5500",
            "http://127.0.0.1:5500",
            "http://192.168.3.193:5500",
            "http://192.168.137.1:5500",
            # Add wildcards for mobile access
            "http://192.168.3.*:5500",
            "http://192.168.*.*:5500"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": True,
        "max_age": 600
    }
})

# Configure rate limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per minute"],
    storage_uri="memory://"
)

try:
    logger.info("Initializing cyberbullying detector...")
    detector = BullyingDetector()
    logger.info("Detector initialization completed")
except Exception as e:
    logger.error(f"Failed to initialize detector: {e}")
    raise

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": datetime.datetime.now().isoformat()})

@app.route('/api/detect', methods=['POST'])
def detect_bullying():
    try:
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json'
            }), 400

        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400

        results = detector.analyze_content(data)
        return jsonify(results), 200

    except Exception as e:
        app.logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            'error': 'Analysis failed',
            'details': str(e)
        }), 500

def _get_recommendations(result):
    """Generate recommendations based on analysis"""
    if not result['combined_result']['is_bullying']:
        return []
        
    severity = result['combined_result']['severity']
    recommendations = [
        "Document and save evidence of bullying",
        "Report the incident to relevant authorities"
    ]
    
    if severity == 'high':
        recommendations.extend([
            "Block and report the sender immediately",
            "Seek support from trusted adults or counselors"
        ])
    
    return recommendations

@app.route('/api/test', methods=['GET'])
def test_route():
    return jsonify({
        "message": "API is working",
        "model_loaded": hasattr(detector, 'classifier')
    })

@app.route('/api/system-check', methods=['GET'])
@limiter.limit("5 per minute")
def system_check():
    try:
        status = {
            "status": "healthy",
            "components": {
                "text_classifier": bool(detector.text_classifier),
                "image_classifier": bool(detector.image_classifier),
                "tesseract": bool(pytesseract.get_tesseract_version()),
            },
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0"
        }
        logger.info(f"System check completed successfully")
        return jsonify(status)
    except Exception as e:
        logger.error(f"System check failed: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Clear and explicit network binding
    try:
        logger.info("Starting server on all interfaces...")
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            threaded=True,
            use_reloader=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise