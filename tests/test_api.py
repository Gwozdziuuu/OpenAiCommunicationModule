#!/usr/bin/env python3
"""
Test script for REST API
"""

import requests
import json
import sys
import os

# Add path to project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import Config

# URL bazowy API
BASE_URL = f"http://localhost:{Config.PORT()}"


def test_health():
    """Test /health endpoint"""
    try:
        response = requests.get(f'{BASE_URL}/health')
        print(f"Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def test_process_without_token():
    """Test /process endpoint without token"""
    try:
        data = {
            "text": "Test message",
            "model": "gpt-4o"
        }
        response = requests.post(
            f'{BASE_URL}/process',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Process without token: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 400
    except Exception as e:
        print(f"Test without token error: {e}")
        return False


def test_process_with_mock_token():
    """Test /process endpoint with mock token (will get OpenAI error, but API works)"""
    try:
        data = {
            "text": "Test message",
            "token": "mock-token-123",
            "model": "gpt-4o"
        }
        response = requests.post(
            f'{BASE_URL}/process',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Process with mock token: {response.status_code}")
        print(f"Response: {response.json()}")
        # Expect 500 error because token is invalid
        return response.status_code == 500
    except Exception as e:
        print(f"Test with mock token error: {e}")
        return False


def main():
    """Main test function"""
    print("=== TESTING REST API ===")
    print()
    print("WARNING: Start server first: python3 -m src.api.server")
    print(f"Testing on: {BASE_URL}")
    print()
    
    tests = [
        ("Health Check", test_health),
        ("Models Endpoint", test_models),
        ("Process without token", test_process_without_token),
        ("Process with mock token", test_process_with_mock_token)
    ]
    
    for test_name, test_func in tests:
        print(f"--- {test_name} ---")
        success = test_func()
        print(f"Status: {'✅ PASS' if success else '❌ FAIL'}")
        print()


if __name__ == '__main__':
    main()