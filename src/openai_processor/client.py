#!/usr/bin/env python3
"""
OpenAI client for processing messages with text and images
"""

import sys
import os
from typing import Optional
from openai import OpenAI

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import Config


class OpenAIClient:
    """Class for communication with OpenAI API"""
    
    def __init__(self, api_token: str):
        """
        Initialize OpenAI client
        
        Args:
            api_token: OpenAI API authorization token
        """
        if not api_token:
            raise ValueError("Authorization token is required")
        
        self.client = OpenAI(api_key=api_token)
    
    def process_message(self, text: str, image_url: Optional[str] = None, 
                       model: str = None) -> str:
        """
        Process message using OpenAI API
        
        Args:
            text: Message text
            image_url: URL to image (optional)
            model: AI model to use
        
        Returns:
            Response from OpenAI
        """
        if not text:
            raise ValueError("Message text is required")
        
        if not model:
            raise ValueError("Model parameter is required")
        
        messages = []
        
        if image_url:
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            })
        else:
            messages.append({
                "role": "user",
                "content": text
            })
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=Config.MAX_TOKENS()
            )
            
            # Return both content and token information
            return {
                "content": response.choices[0].message.content,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        
        except Exception as e:
            raise Exception(f"Error during OpenAI communication: {str(e)}")


def process_message(text: str, image_url: Optional[str] = None, 
                   api_token: str = "", model: str = None) -> str:
    """
    Helper function for processing messages (backwards compatibility)
    
    Args:
        text: Message text
        image_url: URL to image (optional)
        api_token: OpenAI authorization token
        model: AI model to use
    
    Returns:
        Response from OpenAI
    """
    if not model:
        raise ValueError("Model parameter is required")
    client = OpenAIClient(api_token)
    return client.process_message(text, image_url, model)