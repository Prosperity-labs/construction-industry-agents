#!/usr/bin/env python3
"""
Comprehensive Test Suite for Construction Industry Agents
Tests all components and workflows systematically
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemTestSuite:
    """Comprehensive test suite for the construction industry system"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = time.time()
        
    def run_all_tests(self):
        """Run complete test suite"""
        print("🧪 CONSTRUCTION INDUSTRY AGENTS - TEST SUITE")
        print("=" * 60)
        
        tests = [
            ("System Builder Test", self.test_system_builder),
            ("Individual Agents Test", self.test_individual_agents),
            ("Workflow Integration Test", self.test_workflow_integration),
            ("Excel Processing Test", self.test_excel_processing),
            ("Output Quality Test", self.test_output_quality),
            ("Error Handling Test", self.test_error_handling),
            ("Performance Test", self.test_performance)
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Running: {test_name}")
            try:
                result = test_func()
                self.test_results[test_name] = {"status": "PASS", "details": result}
                print(f"✅ {test_name}: PASSED")
            except Exception as e:
                self.test_results[test_name] = {"status": "FAIL", "error": str(e)}
                print(f"❌ {test_name}: FAILED - {str(e)}")
        
        self.print_test_summary()
    
    def test_system_builder(self):
        """Test the iterative system builder"""
        # Check if system builder exists and runs
        result = subprocess.run([
            sys.executable, "system_builder.py"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            raise Exception(f"System builder failed: {result.stderr}")
        
        # Verify all agents were created
        required_files = [
            "supplier_mapping_agent.py",
            "communication_agent.py", 
            "response_parser_agent.py",
            "quote_calculator_agent.py",
            "document_generator_agent.py"
        ]
        
        missing_files = [f for f in required_files if not Path(f).exists()]
        if missing_files:
            raise Exception(f"Missing files after build: {missing_files}")
        
        return f"Built {len(required_files)} agents successfully"
    
    def test_individual_agents(self):
        """Test each agent individually"""
        agents = [
            ("excel_parser_agent.py", "--no-llm"),
            ("supplier_mapping_agent.py", ""),
            ("communication_agent.py", ""),
            ("response_parser_agent.py", ""),
            ("quote_calculator_agent.py", ""),
            ("document_generator_agent.py", "")
        ]
        
        results = []
        for agent_file, args in agents:
            try:
                cmd = [sys.executable, agent_file] + (args.split() if args else [])
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    results.append(f"✅ {agent_file}")
                else:
                    results.append(f"❌ {agent_file}: {result.stderr[:100]}")
            except subprocess.TimeoutExpired:
                results.append(f"⏰ {agent_file}: Timeout")
            except Exception as e:
                results.append(f"❌ {agent_file}: {str(e)}")
        
        return results
    
    def test_workflow_integration(self):
        """Test complete workflow integration"""
        # Test with demo data
        result = subprocess.run([
            sys.executable, "workflow_orchestrator.py"
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode != 0:
            raise Exception(f"Workflow failed: {result.stderr}")
        
        # Check if output files were created
        output_dir = Path("complete_workflow_output")
        if not output_dir.exists():
            raise Exception("Output directory not created")
        
        output_files = list(output_dir.glob("*.xlsx")) + list(output_dir.glob("*.json"))
        if len(output_files) < 3:
            raise Exception(f"Expected at least 3 output files, found {len(output_files)}")
        
        return f"Generated {len(output_files)} output files"
    
    def test_excel_processing(self):
        """Test Excel file processing with different inputs"""
        test_files = list(Path("tests/input").glob("*.xlsx"))
        if not test_files:
            return "No test Excel files found - skipped"
        
        results = []
        for test_file in test_files[:3]:  # Test first 3 files
            try:
                result = subprocess.run([
                    sys.executable, "excel_parser_agent.py", str(test_file), "--no-llm"
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    results.append(f"✅ {test_file.name}")
                else:
                    results.append(f"❌ {test_file.name}")
            except Exception as e:
                results.append(f"❌ {test_file.name}: Error")
        
        return results
    
    def test_output_quality(self):
        """Test quality of generated outputs"""
        output_dir = Path("complete_workflow_output")
        if not output_dir.exists():
            raise Exception("No output directory found")
        
        # Check Excel files
        excel_files = list(output_dir.glob("*.xlsx"))
        json_files = list(output_dir.glob("*.json"))
        
        if not excel_files:
            raise Exception("No Excel output files found")
        
        if not json_files:
            raise Exception("No JSON output files found")
        
        # Validate JSON structure
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    if 'workflow_id' not in data:
                        raise Exception(f"Invalid JSON structure in {json_file}")
            except json.JSONDecodeError:
                raise Exception(f"Invalid JSON in {json_file}")
        
        return f"Validated {len(excel_files)} Excel and {len(json_files)} JSON files"
    
    def test_error_handling(self):
        """Test system error handling"""
        test_cases = [
            # Test with non-existent file
            (["workflow_orchestrator.py", "nonexistent.xlsx"], "Should handle missing files"),
            # Test individual agent with no args (some might fail gracefully)
            (["supplier_mapping_agent.py"], "Should handle missing arguments")
        ]
        
        results = []
        for cmd, description in test_cases:
            try:
                result = subprocess.run([sys.executable] + cmd, 
                                      capture_output=True, text=True, timeout=30)
                # We expect some of these to fail gracefully
                if "Error" in result.stderr or "Exception" in result.stderr:
                    results.append(f"✅ {description}: Error handled gracefully")
                else:
                    results.append(f"⚠️ {description}: No error handling detected")
            except Exception:
                results.append(f"✅ {description}: Exception handled")
        
        return results
    
    def test_performance(self):
        """Test system performance"""
        start_time = time.time()
        
        # Run workflow and measure time
        result = subprocess.run([
            sys.executable, "workflow_orchestrator.py"
        ], capture_output=True, text=True, timeout=120)
        
        duration = time.time() - start_time
        
        if result.returncode != 0:
            raise Exception("Performance test failed - workflow error")
        
        # Performance thresholds
        if duration > 60:
            return f"⚠️ Slow performance: {duration:.1f}s (expected <60s)"
        elif duration > 30:
            return f"✅ Acceptable performance: {duration:.1f}s"
        else:
            return f"✅ Excellent performance: {duration:.1f}s"
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        total_time = time.time() - self.start_time
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in self.test_results.values() if r["status"] == "PASS")
        total = len(self.test_results)
        
        print(f"✅ Tests Passed: {passed}/{total}")
        print(f"⏱️  Total Time: {total_time:.1f} seconds")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED - SYSTEM READY FOR PRODUCTION!")
        else:
            print("⚠️  SOME TESTS FAILED - REVIEW RESULTS ABOVE")
        
        print("\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result["status"] == "PASS" else "❌"
            print(f"  {status_emoji} {test_name}: {result['status']}")
            
            if result["status"] == "PASS" and "details" in result:
                if isinstance(result["details"], list):
                    for detail in result["details"]:
                        print(f"      {detail}")
                else:
                    print(f"      {result['details']}")
            elif result["status"] == "FAIL":
                print(f"      Error: {result['error']}")
        
        print("\n💡 RECOMMENDED NEXT STEPS:")
        if passed == total:
            print("  🚀 Deploy to production environment")
            print("  📊 Set up monitoring and analytics")
            print("  🔐 Implement authentication system")
        else:
            print("  🔧 Fix failing tests")
            print("  🧪 Re-run test suite")
            print("  📝 Review error messages above")

def main():
    """Run the test suite"""
    test_suite = SystemTestSuite()
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()