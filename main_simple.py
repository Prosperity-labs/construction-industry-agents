#!/usr/bin/env python3
"""
Construction Industry Agents - Simple Main Entry Point
Works with the restructured codebase
"""

import sys
import argparse
from pathlib import Path

def main():
    """Simple main entry point that works with current structure"""
    parser = argparse.ArgumentParser(description="Construction Industry Agents")
    parser.add_argument("command", choices=["workflow", "web", "test", "demo"], 
                       help="Command to run")
    parser.add_argument("--file", help="Excel file to process")
    parser.add_argument("--port", type=int, default=5000, help="Web server port")
    
    args = parser.parse_args()
    
    if args.command == "workflow":
        print("🚀 Running workflow...")
        import subprocess
        subprocess.run([sys.executable, "src/workflow/orchestrators/workflow_orchestrator.py"])
        
    elif args.command == "web":
        print("🌐 Starting web frontend...")
        import subprocess
        subprocess.run([sys.executable, "src/web/frontend/app.py"])
        
    elif args.command == "test":
        print("🧪 Running tests...")
        import subprocess
        subprocess.run([sys.executable, "src/testing/framework/test_runner.py"])
        
    elif args.command == "demo":
        print("🎬 Starting demo...")
        import subprocess
        subprocess.run([sys.executable, "scripts/launch_demo.py"])

if __name__ == "__main__":
    main()