#!/usr/bin/env python3
"""
REST API Server for OpenAI application
"""

from flask import Flask, jsonify
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import Config
from api.endpoints.health import HealthEndpoint
from api.endpoints.process import ProcessEndpoint


def create_app():
    """Factory function for creating Flask application"""
    app = Flask(__name__)
    logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL()))
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return HealthEndpoint.health_check()

    @app.route('/process', methods=['POST'])
    def process_openai_message():
        return ProcessEndpoint.process_openai_message()

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