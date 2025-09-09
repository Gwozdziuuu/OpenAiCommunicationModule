#!/usr/bin/env python3
"""
Basic usage examples for OpenAI application
"""

import sys
import os
import json

# Add path to project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from openai_processor.client import OpenAIClient, process_message


def example_text_only():
    """Przykład 1: Tylko tekst"""
    print("=== Przykład 1: Tylko tekst ===")
    try:
        # UWAGA: Zastąp 'your-api-key-here' prawdziwym kluczem API
        client = OpenAIClient("your-api-key-here")
        response = client.process_message(
            text="Napisz krótki wiersz o technologii",
            model="gpt-4o"
        )
        print("Response:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
    print()


def example_with_image():
    """Przykład 2: Tekst z obrazkiem"""
    print("=== Przykład 2: Tekst z obrazkiem ===")
    try:
        # Używanie funkcji pomocniczej dla kompatybilności wstecznej
        response = process_message(
            text="Co widzisz na tym obrazku?",
            image_url="https://example.com/image.jpg",
            api_token="your-api-key-here",
            model="gpt-4o"
        )
        print("Response:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")
    print()


def example_json_format():
    """Przykład 3: Format danych JSON"""
    print("=== Przykład 3: Format danych JSON ===")
    data = {
        "text": "Wytłumacz mi co to jest sztuczna inteligencja",
        "image_url": None,
        "token": "your-api-key-here",
        "model": "gpt-3.5-turbo"
    }
    
    print("Przykład danych JSON:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print()


def example_interactive():
    """Przykład 4: Tryb interaktywny"""
    print("=== Przykład 4: Tryb interaktywny ===")
    print("Ten przykład pokazuje jak zbierać dane od użytkownika")
    
    # Symulacja danych wejściowych
    sample_inputs = {
        "text": "Napisz krótką historię o kocie",
        "image_url": "",  # Puste - bez obrazka
        "api_token": "your-api-key-here",
        "model": "gpt-4o"
    }
    
    print("Przykładowe dane wejściowe:")
    for key, value in sample_inputs.items():
        if value:
            print(f"{key}: {value}")
        else:
            print(f"{key}: (puste)")
    print()


def main():
    """Główna funkcja z przykładami"""
    print("🤖 OPENAI MESSAGE PROCESSOR USAGE EXAMPLES")
    print("=" * 50)
    print()
    
    print("📖 Running instructions:")
    print()
    print("1. Aplikacja interaktywna:")
    print("   python3 -m src.openai_processor.app")
    print()
    print("2. Serwer REST API:")
    print("   python3 -m src.api.server")
    print()
    print("3. Testy:")
    print("   python3 tests/test_api.py")
    print("   python3 tests/test_client.py")
    print()
    
    # Run examples
    example_text_only()
    example_with_image()
    example_json_format()
    example_interactive()


if __name__ == "__main__":
    main()