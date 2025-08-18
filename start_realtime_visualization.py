#!/usr/bin/env python3
"""
Startup Script for Realtime Workflow Visualization
Easy launcher for the realtime workflow visualization system
"""

import os
import sys
import subprocess
import time
import webbrowser
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import flask_cors
        logger.info("✅ Flask dependencies found")
        return True
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        logger.info("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_port_available(port: int) -> bool:
    """Check if port is available"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def start_mock_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the mock SSE server"""
    logger.info(f"🚀 Starting Mock SSE Server on {host}:{port}")
    
    # Check if port is available
    if not check_port_available(port):
        logger.error(f"❌ Port {port} is already in use")
        logger.info("Please stop any existing server or use a different port")
        return False
    
    try:
        # Import and start the server
        from mock_sse_server import MockSSEServer
        
        server = MockSSEServer(host, port)
        logger.info("✅ Mock SSE Server started successfully")
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            url = f"http://localhost:{port}"
            logger.info(f"🌐 Opening dashboard at {url}")
            webbrowser.open(url)
        
        # Start browser in background thread
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Run the server
        server.run(debug=False)
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Failed to start server: {e}")
        return False
    
    return True

def run_tests():
    """Run the test suite"""
    logger.info("🧪 Running test suite...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_realtime_visualization.py"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            logger.info("✅ All tests passed")
            return True
        else:
            logger.error(f"❌ Tests failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error("❌ Tests timed out")
        return False
    except Exception as e:
        logger.error(f"❌ Failed to run tests: {e}")
        return False

def show_help():
    """Show help information"""
    print("""
🏗️ Construction Industry Agents - Realtime Workflow Visualization

Usage:
  python start_realtime_visualization.py [options]

Options:
  --help, -h          Show this help message
  --test, -t          Run test suite only
  --port PORT         Use specific port (default: 8000)
  --host HOST         Use specific host (default: 0.0.0.0)
  --no-browser        Don't open browser automatically
  --docker            Use Docker instead of local Python

Examples:
  python start_realtime_visualization.py
  python start_realtime_visualization.py --port 8080
  python start_realtime_visualization.py --test
  python start_realtime_visualization.py --docker

Features:
  ✅ Real-time workflow monitoring
  ✅ Interactive dashboard
  ✅ Mock SSE server
  ✅ Docker support
  ✅ Comprehensive testing
  ✅ Performance metrics
""")

def start_with_docker():
    """Start the system using Docker"""
    logger.info("🐳 Starting with Docker...")
    
    try:
        # Check if Docker is available
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("❌ Docker not found. Please install Docker first.")
            return False
        
        # Check if docker-compose is available
        result = subprocess.run(["docker-compose", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("❌ Docker Compose not found. Please install Docker Compose first.")
            return False
        
        # Start the services
        logger.info("🚀 Starting Docker services...")
        subprocess.run(["docker-compose", "up", "mock-sse-server"], check=True)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Docker command failed: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("\n🛑 Stopping Docker services...")
        subprocess.run(["docker-compose", "down"])
        return True
    except Exception as e:
        logger.error(f"❌ Failed to start Docker: {e}")
        return False
    
    return True

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Start Realtime Workflow Visualization",
        add_help=False
    )
    parser.add_argument("--help", "-h", action="store_true", help="Show help message")
    parser.add_argument("--test", "-t", action="store_true", help="Run test suite only")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    parser.add_argument("--host", default="0.0.0.0", help="Server host (default: 0.0.0.0)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    parser.add_argument("--docker", action="store_true", help="Use Docker instead of local Python")
    
    args = parser.parse_args()
    
    # Show help if requested
    if args.help:
        show_help()
        return 0
    
    # Print welcome message
    print("🏗️ Construction Industry Agents")
    print("Realtime Workflow Visualization - v1")
    print("=" * 50)
    
    # Run tests only if requested
    if args.test:
        return 0 if run_tests() else 1
    
    # Check dependencies
    if not args.docker and not check_dependencies():
        return 1
    
    # Start the system
    if args.docker:
        success = start_with_docker()
    else:
        success = start_mock_server(args.host, args.port)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 