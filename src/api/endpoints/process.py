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
            'model': data.get('model', '').strip(),
            'response_format': data.get('response_format'),
            'output_example': data.get('output_example')
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
    def _prepare_response_format(params):
        """Prepare response format from output_example or response_format"""
        if params['output_example']:
            # Convert example to JSON schema
            import json
            try:
                example = json.loads(params['output_example']) if isinstance(params['output_example'], str) else params['output_example']
                schema = ProcessEndpoint._generate_schema_from_example(example)
                return {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "response",
                        "schema": schema
                    }
                }
            except (json.JSONDecodeError, TypeError):
                logging.warning("Invalid output_example format, ignoring")
                return params['response_format']
        return params['response_format']
    
    @staticmethod
    def _generate_schema_from_example(example):
        """Generate JSON schema from example object"""
        def get_type_from_value(value):
            if isinstance(value, str):
                return "string"
            elif isinstance(value, int):
                return "integer" 
            elif isinstance(value, float):
                return "number"
            elif isinstance(value, bool):
                return "boolean"
            elif isinstance(value, list):
                return "array"
            elif isinstance(value, dict):
                return "object"
            else:
                return "string"
        
        def build_schema(obj):
            if isinstance(obj, dict):
                properties = {}
                for key, value in obj.items():
                    if isinstance(value, dict):
                        properties[key] = build_schema(value)
                    elif isinstance(value, list) and len(value) > 0:
                        properties[key] = {
                            "type": "array",
                            "items": build_schema(value[0]) if isinstance(value[0], dict) else {"type": get_type_from_value(value[0])}
                        }
                    else:
                        properties[key] = {"type": get_type_from_value(value)}
                
                return {
                    "type": "object",
                    "properties": properties,
                    "required": list(properties.keys())
                }
            else:
                return {"type": get_type_from_value(obj)}
        
        return build_schema(example)
    
    @staticmethod
    def _log_processing_info(model, image_url):
        """Log processing information"""
        logging.info(f"Processing message for model: {model}")
        if image_url:
            logging.info(f"With image: {image_url}")
    
    @staticmethod
    def _build_success_response(response, model, image_url, was_structured=False):
        """Build successful response JSON"""
        import json
        
        content = response["content"]
        
        # If it was a structured response, try to parse the JSON
        if was_structured and isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                # If parsing fails, keep as string
                pass
        
        return jsonify({
            "success": True,
            "response": content,
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
            "model": "gpt-4o",  // required
            "output_example": {  // optional - simple example, AI will match format
                "description": "A beautiful sunset over mountains",
                "objects": ["mountain", "sky", "clouds"],
                "mood": "peaceful"
            }
        }
        
        Alternative with explicit response_format:
        {
            "text": "message content",
            "response_format": {  // optional - explicit JSON Schema
                "type": "json_schema",
                "json_schema": {
                    "name": "response",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "answer": {"type": "string"}
                        }
                    }
                }
            }
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
        
        # Prepare response format
        prepared_format = ProcessEndpoint._prepare_response_format(params)
        
        # Process message (only this part can actually throw exceptions)
        try:
            response = process_message(
                text=params['text'],
                image_url=params['image_url'],
                api_token=params['api_token'],
                model=params['model'],
                response_format=prepared_format
            )
            
            return ProcessEndpoint._build_success_response(
                response, params['model'], params['image_url'], 
                was_structured=bool(prepared_format)
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