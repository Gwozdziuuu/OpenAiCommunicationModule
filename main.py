#!/usr/bin/env python3
"""
Main entry point for OpenAI Message Processor application
"""

import sys
import os

# Add path to project modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def show_help():
    """Display help for available commands"""
    print("🤖 OpenAI Message Processor")
    print("=" * 50)
    print()
    print("Available commands:")
    print()
    print("  python3 main.py app        - Run console application")
    print("  python3 main.py server     - Run REST API server")
    print("  python3 main.py test       - Run API tests")
    print("  python3 main.py examples   - Show usage examples")
    print("  python3 main.py help       - Show this help")
    print()
    print("Alternative ways to run:")
    print()
    print("  python3 -m src.openai_processor.app")
    print("  python3 -m src.api.server")
    print("  python3 tests/test_api.py")
    print("  python3 examples/basic_usage.py")
    print()


def main():
    """Main routing function"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "app":
        from src.openai_processor.app import main as app_main
        app_main()
    
    elif command == "server":
        from src.api.server import main as server_main
        server_main()
    
    elif command == "test":
        from tests.test_api import main as test_main
        test_main()
    
    elif command == "examples":
        from examples.basic_usage import main as examples_main
        examples_main()
    
    elif command == "help":
        show_help()
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'python3 main.py help' to see available commands.")


if __name__ == "__main__":
    main()