#!/usr/bin/env python3
"""
Application configuration with environment variables
"""

import os


class Config:
    """Configuration class with default values"""
    
    @classmethod
    def get_host(cls):
        return os.getenv('HOST', '0.0.0.0')
    
    @classmethod
    def get_port(cls):
        return int(os.getenv('PORT', '8090'))
    
    @classmethod
    def get_debug(cls):
        return os.getenv('DEBUG', 'true').lower() in ('true', '1', 'yes', 'on')
    
    @classmethod
    def get_default_model(cls):
        return os.getenv('OPENAI_DEFAULT_MODEL', 'gpt-4o')
    
    @classmethod
    def get_max_tokens(cls):
        return int(os.getenv('OPENAI_MAX_TOKENS', '1000'))
    
    @classmethod
    def get_require_token(cls):
        return os.getenv('REQUIRE_TOKEN', 'true').lower() in ('true', '1', 'yes', 'on')
    
    @classmethod
    def get_log_level(cls):
        return os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # For backwards compatibility - aliases
    @classmethod
    def HOST(cls):
        return cls.get_host()
    
    @classmethod
    def PORT(cls):
        return cls.get_port()
    
    @classmethod
    def DEBUG(cls):
        return cls.get_debug()
    
    @classmethod
    def DEFAULT_MODEL(cls):
        return cls.get_default_model()
    
    @classmethod
    def MAX_TOKENS(cls):
        return cls.get_max_tokens()
    
    @classmethod
    def REQUIRE_TOKEN(cls):
        return cls.get_require_token()
    
    @classmethod
    def LOG_LEVEL(cls):
        return cls.get_log_level()

    @classmethod
    def show_config(cls):
        """Display current configuration"""
        print("App configuration:")
        print(f"   HOST: {cls.HOST()}")
        print(f"   PORT: {cls.PORT()}")
        print(f"   DEBUG: {cls.DEBUG()}")
        print(f"   DEFAULT_MODEL: {cls.DEFAULT_MODEL()}")
        print(f"   MAX_TOKENS: {cls.MAX_TOKENS()}")
        print(f"   REQUIRE_TOKEN: {cls.REQUIRE_TOKEN()}")
        print(f"   LOG_LEVEL: {cls.LOG_LEVEL()}")
        print()


def load_env_file(filepath='.env'):
    """
    Load environment variables from .env file (optional)
    """
    possible_paths = [
        filepath,  # Relative path from CWD
        os.path.join(os.getcwd(), filepath),  # Explicit CWD
        os.path.join(os.path.dirname(__file__), '..', filepath),  # Relative to config.py
        os.path.join(os.path.dirname(__file__), '..', '..', filepath)  # Two levels up
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Loading configuration from: {path}")
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            # Only set variable if not already set
                            if key.strip() not in os.environ:
                                os.environ[key.strip()] = value.strip().strip('"\'')
            return
    
    print(".env file not found - using default values")


# Automatically load .env if it exists
load_env_file()