#!/usr/bin/env python3
"""
Setup script for Construction Industry Agents
"""

import subprocess
import sys
from pathlib import Path

def setup_environment():
    """Set up the development environment"""
    print("🏗️ Setting up Construction Industry Agents...")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # Install requirements
    print("📋 Installing requirements...")
    pip_cmd = "venv/bin/pip" if sys.platform != "win32" else "venv\\Scripts\\pip"
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"])
    
    # Run system builder
    print("🔨 Building system components...")
    python_cmd = "venv/bin/python" if sys.platform != "win32" else "venv\\Scripts\\python"
    subprocess.run([python_cmd, "src/workflow/builders/system_builder.py"])
    
    print("✅ Setup completed!")
    print("🚀 Run: python main.py demo")

if __name__ == "__main__":
    setup_environment()
