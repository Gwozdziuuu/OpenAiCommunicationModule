#!/usr/bin/env python3
"""
Unit tests for OpenAI client
"""

import pytest
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
    with pytest.raises(ValueError, match="Authorization token is required"):
        OpenAIClient("")


def test_process_message_validation():
    """Test parameter validation"""
    # Test without text
    with pytest.raises(ValueError, match="Message text is required"):
        client = OpenAIClient("test-token")
        client.process_message("")
    
    # Test without token in helper function
    with pytest.raises(ValueError, match="Authorization token is required"):
        process_message("test", api_token="")


if __name__ == '__main__':
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