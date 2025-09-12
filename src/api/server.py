#!/usr/bin/env python3
"""
REST API Server for OpenAI application
"""

from flask import Flask, request, jsonify
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from openai_processor.client import process_message
from config import Config


def create_app():
    """Factory function for creating Flask application"""
    app = Flask(__name__)
    logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL()))
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Server health check endpoint
        """
        return jsonify({
            "status": "healthy",
            "service": "OpenAI Message Processor"
        }), 200

    @app.route('/process', methods=['POST'])
    def process_openai_message():
        """
        Endpoint for processing messages through OpenAI
        
        Expected JSON data:
        {
            "text": "message content",
            "image_url": "http://example.com/image.jpg",  // optional
            "token": "openai-api-token",  // required
            "model": "gpt-4o"  // required
        }
        """
        try:
            if not request.is_json:
                return jsonify({
                    "error": "Content-Type must be application/json"
                }), 400
            
            data = request.get_json()
            
            if not data:
                return jsonify({
                    "error": "No JSON data in request"
                }), 400
            
            # Get parameters
            text = data.get('text', '').strip()
            image_url = data.get('image_url')
            api_token = data.get('token', '').strip()
            model = data.get('model', '').strip()
            
            # Validate required fields
            if not text:
                return jsonify({
                    "error": "Field 'text' is required and cannot be empty"
                }), 400
            
            if not api_token:
                return jsonify({
                    "error": "Field 'token' is required"
                }), 400
                
            if not model:
                return jsonify({
                    "error": "Field 'model' is required"
                }), 400
            
            # Process message
            logging.info(f"Processing message for model: {model}")
            if image_url:
                logging.info(f"With image: {image_url}")
            
            response = process_message(
                text=text,
                image_url=image_url,
                api_token=api_token,
                model=model
            )
            
            return jsonify({
                "success": True,
                "response": response["content"],
                "model_used": model,
                "has_image": bool(image_url),
                "usage": response["usage"]
            }), 200
            
        except ValueError as e:
            logging.error(f"Validation error: {str(e)}")
            return jsonify({
                "error": str(e)
            }), 400
            
        except Exception as e:
            logging.error(f"Server error: {str(e)}")
            return jsonify({
                "error": f"Error during processing: {str(e)}"
            }), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Endpoint not found",
            "available_endpoints": [
                "GET /health - server health check",
                "POST /process - process messages",
                "GET /models - available models"
            ]
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "HTTP method not allowed for this endpoint"
        }), 405
    
    return app


def main():
    """Main function to start the server"""
    app = create_app()
    
    print("🚀 Starting REST API for OpenAI Message Processor")
    print("📍 Available endpoints:")
    print("   GET  /health  - health check")
    print("   POST /process - process messages")
    print("   GET  /models  - available models")
    print()
    
    Config.show_config()
    
    app.run(
        host=Config.HOST(),
        port=Config.PORT(),
        debug=Config.DEBUG()
    )


if __name__ == '__main__':
    main()