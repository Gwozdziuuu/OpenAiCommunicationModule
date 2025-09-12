#!/usr/bin/env python3
"""
Message processing endpoint handler
"""

from flask import request, jsonify
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from openai_processor.client import process_message


class ProcessEndpoint:
    """Handler for message processing endpoint"""
    
    @staticmethod
    def _validate_request_format():
        """Validate request format and extract JSON data"""
        if not request.is_json:
            return None, jsonify({
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        if not data:
            return None, jsonify({
                "error": "No JSON data in request"
            }), 400
            
        return data, None, None
    
    @staticmethod
    def _extract_parameters(data):
        """Extract and return parameters from request data"""
        return {
            'text': data.get('text', '').strip(),
            'image_url': data.get('image_url'),
            'api_token': data.get('token', '').strip(),
            'model': data.get('model', '').strip()
        }
    
    @staticmethod
    def _validate_required_fields(params):
        """Validate required fields and return error response if invalid"""
        if not params['text']:
            return jsonify({
                "error": "Field 'text' is required and cannot be empty"
            }), 400
        
        if not params['api_token']:
            return jsonify({
                "error": "Field 'token' is required"
            }), 400
            
        if not params['model']:
            return jsonify({
                "error": "Field 'model' is required"
            }), 400
            
        return None, None
    
    @staticmethod
    def _log_processing_info(model, image_url):
        """Log processing information"""
        logging.info(f"Processing message for model: {model}")
        if image_url:
            logging.info(f"With image: {image_url}")
    
    @staticmethod
    def _build_success_response(response, model, image_url):
        """Build successful response JSON"""
        return jsonify({
            "success": True,
            "response": response["content"],
            "model_used": model,
            "has_image": bool(image_url),
            "usage": response["usage"]
        }), 200
    
    @staticmethod
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
        # Validate request format
        data, error_response, status_code = ProcessEndpoint._validate_request_format()
        if error_response:
            return error_response, status_code
        
        # Extract parameters
        params = ProcessEndpoint._extract_parameters(data)
        
        # Validate required fields
        error_response, status_code = ProcessEndpoint._validate_required_fields(params)
        if error_response:
            return error_response, status_code
        
        # Log processing information
        ProcessEndpoint._log_processing_info(params['model'], params['image_url'])
        
        # Process message (only this part can actually throw exceptions)
        try:
            response = process_message(
                text=params['text'],
                image_url=params['image_url'],
                api_token=params['api_token'],
                model=params['model']
            )
            
            return ProcessEndpoint._build_success_response(
                response, params['model'], params['image_url']
            )
            
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