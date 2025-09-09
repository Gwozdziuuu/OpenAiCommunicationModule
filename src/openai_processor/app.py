#!/usr/bin/env python3
"""
OpenAI Message Processor console application
"""

import sys
import json
from .client import process_message


def main():
    """
    Main application function - expects input data
    """
    print("OpenAI Message Processor")
    print("Enter data in JSON format or interactively:")
    print()
    
    try:
        # Check if data was passed as argument
        if len(sys.argv) > 1:
            input_data = sys.argv[1]
            try:
                data = json.loads(input_data)
                text = data.get("text", "")
                image_url = data.get("image_url")
                api_token = data.get("token", "")
                model = data.get("model", "gpt-4o")
            except json.JSONDecodeError:
                print("Error: Invalid JSON format")
                return
        else:
            # Interactive mode
            text = input("Enter message text: ").strip()
            image_url = input("Image URL (optional, press Enter to skip): ").strip() or None
            api_token = input("OpenAI Token: ").strip()
            model = input("AI Model (default gpt-4o): ").strip() or "gpt-4o"
        
        if not text:
            print("Error: Message text is required")
            return
            
        if not api_token:
            print("Error: OpenAI token is required")
            return
        
        print(f"\nProcessing message using model {model}...")
        if image_url:
            print(f"With image: {image_url}")
        
        response = process_message(text, image_url, api_token, model)
        
        print("\n" + "="*50)
        print("OPENAI RESPONSE:")
        print("="*50)
        print(response["content"])
        
        print("\n" + "="*25)
        print("TOKEN USAGE:")
        print("="*25)
        usage = response["usage"]
        print(f"Prompt tokens: {usage['prompt_tokens']}")
        print(f"Completion tokens: {usage['completion_tokens']}")
        print(f"Total tokens: {usage['total_tokens']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return


if __name__ == "__main__":
    main()