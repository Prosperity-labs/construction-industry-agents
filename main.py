#!/usr/bin/env python3
"""
Construction Industry Agents - Main Application Entry Point
"""

import sys
import argparse
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.workflow.orchestrators.workflow_orchestrator import WorkflowOrchestrator
from src.web.frontend.app import create_app
from src.testing.framework.test_runner import TestRunner

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Construction Industry Agents")
    parser.add_argument("command", choices=["workflow", "web", "test", "demo"], 
                       help="Command to run")
    parser.add_argument("--file", help="Excel file to process")
    parser.add_argument("--port", type=int, default=5000, help="Web server port")
    
    args = parser.parse_args()
    
    if args.command == "workflow":
        orchestrator = WorkflowOrchestrator()
        if args.file:
            orchestrator.run_workflow(args.file)
        else:
            orchestrator.run_demo_workflow()
            
    elif args.command == "web":
        app = create_app()
        app.run(host="0.0.0.0", port=args.port, debug=True)
        
    elif args.command == "test":
        runner = TestRunner()
        runner.run_all_tests()
        
    elif args.command == "demo":
        from scripts.launch_demo import main as demo_main
        demo_main()

if __name__ == "__main__":
    main()
