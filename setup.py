#!/usr/bin/env python3
"""
Setup script for Multi-Agent Debate System
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Set up the multi-agent debate system."""
    print("🚀 Setting up Multi-Agent Debate System")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Check for .env file
    if not os.path.exists(".env"):
        print("⚠️  No .env file found. Creating from template...")
        if os.path.exists("env_example.txt"):
            run_command("cp env_example.txt .env", "Creating .env file")
            print("📝 Please edit .env and add your OpenAI API key")
        else:
            print("❌ env_example.txt not found")
            sys.exit(1)
    else:
        print("✅ .env file found")
    
    # Test import
    print("🧪 Testing imports...")
    try:
        import crewai
        import langchain_openai
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env and add your OpenAI API key")
    print("2. Run: python multi_agent_debate.py")
    print("3. Or run experiments: python run_experiments.py")

if __name__ == "__main__":
    main()
