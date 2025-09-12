#!/usr/bin/env python3
"""
Unit tests for OpenAI client
"""

import sys
import os

# Add path to project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from openai_processor.client import OpenAIClient, process_message


def test_openai_client_init():
    """Test OpenAI client initialization"""
    # Test with valid token
    client = OpenAIClient("test-token")
    assert client.client is not None
    
    # Test without token
    try:
        OpenAIClient("")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Authorization token is required" in str(e)


def test_process_message_validation():
    """Test parameter validation"""
    client = OpenAIClient("test-token")
    
    # Test without text
    try:
        client.process_message("", model="gpt-4o")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Message text is required" in str(e)
    
    # Test without model
    try:
        client.process_message("test", model="")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Model parameter is required" in str(e)
    
    # Test without token in helper function
    try:
        process_message("test", api_token="", model="gpt-4o")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Authorization token is required" in str(e)
    
    # Test without model in helper function
    try:
        process_message("test", api_token="test-token", model="")
        assert False, "Should raise ValueError"
    except ValueError as e:
        assert "Model parameter is required" in str(e)


if __name__ == '__main__':
    print("=== TESTING OPENAI CLIENT ===")
    print()
    
    # Simple tests without pytest
    try:
        test_openai_client_init()
        print("✅ Client initialization test - PASS")
    except Exception as e:
        print(f"❌ Client initialization test - FAIL: {e}")
    
    try:
        test_process_message_validation()
        print("✅ Parameter validation test - PASS")
    except Exception as e:
        print(f"❌ Parameter validation test - FAIL: {e}")
    
    print()
    print("All tests completed!")