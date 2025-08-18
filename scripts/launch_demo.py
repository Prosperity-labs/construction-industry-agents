#!/usr/bin/env python3
"""
Demo Launcher for Construction Industry Agents
Easy way to start different types of demonstrations
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def print_header():
    """Print demo launcher header"""
    print("🏗️" + "=" * 70 + "🏗️")
    print("    CONSTRUCTION INDUSTRY AGENTS - DEMO LAUNCHER")
    print("🏗️" + "=" * 70 + "🏗️")
    print()

def check_dependencies():
    """Check if all dependencies are available"""
    print("🔍 Checking system dependencies...")
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found. Please run:")
        print("   python -m venv venv")
        print("   source venv/bin/activate")
        print("   pip install -r requirements.txt")
        return False
    
    # Check if all agent files exist
    required_files = [
        "excel_parser_agent.py",
        "supplier_mapping_agent.py",
        "communication_agent.py",
        "response_parser_agent.py",
        "quote_calculator_agent.py",
        "document_generator_agent.py",
        "workflow_orchestrator.py",
        "visual_workflow_monitor.py",
        "web_frontend.py"
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        print("   Please run: python system_builder.py")
        return False
    
    print("✅ All dependencies found!")
    return True

def launch_web_demo():
    """Launch the web frontend demo"""
    print("🌐 Starting Web Frontend Demo...")
    print("📊 This will open a browser with real-time visual demonstration")
    print()
    
    try:
        # Start the web server
        process = subprocess.Popen([
            sys.executable, "web_frontend.py"
        ], cwd=os.getcwd())
        
        # Wait a moment for server to start
        print("⏳ Starting server...")
        time.sleep(3)
        
        # Open browser
        print("🌐 Opening browser at http://localhost:5000")
        webbrowser.open("http://localhost:5000")
        
        print("✅ Web demo launched successfully!")
        print("📋 Instructions:")
        print("  1. Click 'Start Live Demo' button")
        print("  2. Watch real-time workflow visualization")
        print("  3. Download generated documents")
        print("  4. Press Ctrl+C here to stop the server")
        print()
        
        # Wait for user to stop
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping web server...")
            process.terminate()
            print("✅ Web server stopped")
        
    except Exception as e:
        print(f"❌ Error starting web demo: {str(e)}")

def launch_terminal_demo():
    """Launch the terminal-based visual demo"""
    print("💻 Starting Terminal Visual Demo...")
    print("📊 This will show step-by-step workflow in your terminal")
    print()
    
    try:
        subprocess.run([sys.executable, "visual_workflow_monitor.py"], check=True)
        print("✅ Terminal demo completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running terminal demo: {str(e)}")
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")

def run_quick_test():
    """Run quick test of the system"""
    print("🧪 Running Quick System Test...")
    print("📊 This will test all components quickly")
    print()
    
    try:
        subprocess.run([sys.executable, "test_runner.py", "quick"], check=True)
        print("✅ Quick test completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running test: {str(e)}")

def run_full_workflow():
    """Run the complete workflow orchestrator"""
    print("🚀 Running Complete Workflow...")
    print("📊 This will process a demo Excel file end-to-end")
    print()
    
    try:
        subprocess.run([sys.executable, "workflow_orchestrator.py"], check=True)
        print("✅ Workflow completed!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running workflow: {str(e)}")

def show_architecture():
    """Show system architecture"""
    print("🏗️ System Architecture Overview:")
    print()
    print("📊 DATA FLOW:")
    print("┌─────────────────────────────────────────────────────────────────┐")
    print("│                                                                 │")
    print("│  🏢 Revit 3D Model                                              │")
    print("│       ↓                                                         │")
    print("│  📋 Excel Schedule Export                                       │")
    print("│       ↓                                                         │")
    print("│  🤖 AI Agent Processing Pipeline                                │")
    print("│       ↓                                                         │")
    print("│  📄 Professional Quote Documents                                │")
    print("│                                                                 │")
    print("└─────────────────────────────────────────────────────────────────┘")
    print()
    print("🤖 AGENT PIPELINE:")
    print("  1. 📊 Excel Parser Agent - Extracts items and specifications")
    print("  2. 🏭 Supplier Mapping Agent - Finds appropriate suppliers")
    print("  3. 📤 Communication Agent - Sends requests to suppliers")
    print("  4. 📥 Response Parser Agent - Processes supplier responses")
    print("  5. 🧮 Quote Calculator Agent - Optimizes pricing")
    print("  6. 📄 Document Generator Agent - Creates professional docs")
    print()

def main():
    """Main demo launcher function"""
    print_header()
    
    # Check dependencies first
    if not check_dependencies():
        return
    
    while True:
        print("🎯 Choose a demonstration option:")
        print()
        print("  1. 🌐 Web Frontend Demo (Recommended)")
        print("     └─ Beautiful web interface with real-time visualization")
        print()
        print("  2. 💻 Terminal Visual Demo")
        print("     └─ Command-line version with live progress")
        print()
        print("  3. 🚀 Complete Workflow")
        print("     └─ Run end-to-end process with Excel file")
        print()
        print("  4. 🧪 Quick System Test")
        print("     └─ Test all components quickly")
        print()
        print("  5. 🏗️ Show Architecture")
        print("     └─ Display system architecture overview")
        print()
        print("  6. 🚪 Exit")
        print()
        
        choice = input("Select option (1-6): ").strip()
        
        if choice == "1":
            launch_web_demo()
        elif choice == "2":
            launch_terminal_demo()
        elif choice == "3":
            run_full_workflow()
        elif choice == "4":
            run_quick_test()
        elif choice == "5":
            show_architecture()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select 1-6.")
        
        print("\n" + "─" * 70)
        input("Press Enter to continue...")
        print()

if __name__ == "__main__":
    main()