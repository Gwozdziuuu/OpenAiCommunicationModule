#!/usr/bin/env python3
"""
Health check endpoint handler
"""

from flask import jsonify


class HealthEndpoint:
    """Handler for health check endpoint"""
    
    @staticmethod
    def health_check():
        """
        Server health check endpoint
        """
        return jsonify({
            "status": "healthy",
            "service": "OpenAI Message Processor"
        }), 200