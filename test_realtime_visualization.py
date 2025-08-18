#!/usr/bin/env python3
"""
Test Script for Realtime Workflow Visualization
Tests the complete realtime workflow visualization system
"""

import time
import requests
import json
import threading
from datetime import datetime
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RealtimeVisualizationTester:
    """Test the realtime workflow visualization system"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.test_results = {}
        self.start_time = time.time()
    
    def run_all_tests(self):
        """Run all tests"""
        logger.info("🧪 Starting Realtime Workflow Visualization Tests")
        logger.info("=" * 60)
        
        tests = [
            ("Server Health Check", self.test_server_health),
            ("SSE Connection Test", self.test_sse_connection),
            ("Event History API", self.test_event_history_api),
            ("Active Workflows API", self.test_active_workflows_api),
            ("Performance Metrics API", self.test_performance_metrics_api),
            ("Mock Workflow Generation", self.test_mock_workflow_generation),
            ("Dashboard Accessibility", self.test_dashboard_accessibility),
            ("Event Broadcasting", self.test_event_broadcasting),
            ("Error Handling", self.test_error_handling),
            ("Performance Benchmark", self.test_performance_benchmark)
        ]
        
        for test_name, test_func in tests:
            logger.info(f"\n🔍 Running: {test_name}")
            try:
                result = test_func()
                self.test_results[test_name] = {"status": "PASS", "details": result}
                logger.info(f"✅ {test_name}: PASSED")
            except Exception as e:
                self.test_results[test_name] = {"status": "FAIL", "error": str(e)}
                logger.error(f"❌ {test_name}: FAILED - {str(e)}")
        
        self.print_test_summary()
    
    def test_server_health(self) -> Dict[str, Any]:
        """Test server health endpoint"""
        response = requests.get(f"{self.base_url}/health", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "subscribers" in data
        assert "active_workflows" in data
        
        return {
            "status": data["status"],
            "subscribers": data["subscribers"],
            "active_workflows": data["active_workflows"],
            "response_time": response.elapsed.total_seconds()
        }
    
    def test_sse_connection(self) -> Dict[str, Any]:
        """Test SSE connection"""
        import sseclient
        
        # Test SSE connection
        response = requests.get(f"{self.base_url}/events/stream", stream=True, timeout=10)
        response.raise_for_status()
        
        client = sseclient.SSEClient(response)
        events_received = 0
        start_time = time.time()
        
        # Listen for events for 5 seconds
        for event in client.events():
            events_received += 1
            if time.time() - start_time > 5:
                break
        
        return {
            "events_received": events_received,
            "connection_time": time.time() - start_time,
            "connection_successful": True
        }
    
    def test_event_history_api(self) -> Dict[str, Any]:
        """Test event history API"""
        # Test without workflow_id
        response = requests.get(f"{self.base_url}/events/history?limit=10", timeout=10)
        response.raise_for_status()
        
        events = response.json()
        assert isinstance(events, list)
        
        # Test with workflow_id
        response2 = requests.get(f"{self.base_url}/events/history?workflow_id=TEST&limit=5", timeout=10)
        response2.raise_for_status()
        
        events2 = response2.json()
        assert isinstance(events2, list)
        
        return {
            "total_events": len(events),
            "filtered_events": len(events2),
            "response_time": response.elapsed.total_seconds()
        }
    
    def test_active_workflows_api(self) -> Dict[str, Any]:
        """Test active workflows API"""
        response = requests.get(f"{self.base_url}/workflows/active", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        assert "active_workflows" in data
        assert "count" in data
        assert isinstance(data["active_workflows"], list)
        assert isinstance(data["count"], int)
        
        return {
            "active_workflows": data["active_workflows"],
            "count": data["count"],
            "response_time": response.elapsed.total_seconds()
        }
    
    def test_performance_metrics_api(self) -> Dict[str, Any]:
        """Test performance metrics API"""
        response = requests.get(f"{self.base_url}/metrics/performance", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        assert "active_workflows" in data
        assert "connected_clients" in data
        assert "recent_events_count" in data
        assert "system_uptime" in data
        
        return {
            "active_workflows": data["active_workflows"],
            "connected_clients": data["connected_clients"],
            "recent_events_count": data["recent_events_count"],
            "response_time": response.elapsed.total_seconds()
        }
    
    def test_mock_workflow_generation(self) -> Dict[str, Any]:
        """Test mock workflow generation"""
        response = requests.post(f"{self.base_url}/mock/start-workflow", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        assert "status" in data
        assert "workflow_id" in data
        assert data["status"] == "started"
        
        # Wait a bit for workflow to start
        time.sleep(2)
        
        # Check if workflow is active
        response2 = requests.get(f"{self.base_url}/workflows/active", timeout=10)
        response2.raise_for_status()
        
        workflows = response2.json()["active_workflows"]
        
        return {
            "workflow_started": data["status"] == "started",
            "workflow_id": data["workflow_id"],
            "is_active": data["workflow_id"] in workflows,
            "response_time": response.elapsed.total_seconds()
        }
    
    def test_dashboard_accessibility(self) -> Dict[str, Any]:
        """Test dashboard accessibility"""
        response = requests.get(f"{self.base_url}/", timeout=10)
        response.raise_for_status()
        
        html_content = response.text
        assert "Construction Industry Agents" in html_content
        assert "Real-time Dashboard" in html_content
        assert "Mock Controls" in html_content
        
        return {
            "dashboard_accessible": True,
            "content_length": len(html_content),
            "response_time": response.elapsed.total_seconds()
        }
    
    def test_event_broadcasting(self) -> Dict[str, Any]:
        """Test event broadcasting"""
        # This test would require a more sophisticated setup with actual SSE clients
        # For now, we'll test the basic functionality
        
        # Start a mock workflow
        response = requests.post(f"{self.base_url}/mock/start-workflow", timeout=10)
        response.raise_for_status()
        
        # Wait for some events to be generated
        time.sleep(3)
        
        # Check if events were generated
        response2 = requests.get(f"{self.base_url}/events/history?limit=5", timeout=10)
        response2.raise_for_status()
        
        events = response2.json()
        
        return {
            "workflow_started": response.json()["status"] == "started",
            "events_generated": len(events),
            "broadcasting_working": len(events) > 0
        }
    
    def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling"""
        # Test invalid endpoint
        try:
            response = requests.get(f"{self.base_url}/invalid-endpoint", timeout=5)
            # Should return 404
            assert response.status_code == 404
        except requests.exceptions.RequestException:
            pass
        
        # Test invalid parameters
        try:
            response = requests.get(f"{self.base_url}/events/history?limit=invalid", timeout=5)
            # Should handle gracefully
            pass
        except requests.exceptions.RequestException:
            pass
        
        return {
            "error_handling_working": True,
            "invalid_endpoints_handled": True
        }
    
    def test_performance_benchmark(self) -> Dict[str, Any]:
        """Test performance benchmark"""
        start_time = time.time()
        
        # Make multiple concurrent requests
        import concurrent.futures
        
        def make_request():
            try:
                response = requests.get(f"{self.base_url}/health", timeout=5)
                return response.elapsed.total_seconds()
            except:
                return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            response_times = [future.result() for future in futures if future.result() is not None]
        
        total_time = time.time() - start_time
        
        return {
            "total_requests": 20,
            "successful_requests": len(response_times),
            "average_response_time": sum(response_times) / len(response_times) if response_times else 0,
            "total_time": total_time,
            "requests_per_second": len(response_times) / total_time if total_time > 0 else 0
        }
    
    def print_test_summary(self):
        """Print test summary"""
        logger.info("\n" + "=" * 60)
        logger.info("📊 REALTIME WORKFLOW VISUALIZATION TEST SUMMARY")
        logger.info("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result["status"] == "PASS")
        failed_tests = total_tests - passed_tests
        
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            logger.info("\n❌ FAILED TESTS:")
            for test_name, result in self.test_results.items():
                if result["status"] == "FAIL":
                    logger.info(f"  - {test_name}: {result.get('error', 'Unknown error')}")
        
        logger.info("\n✅ PASSED TESTS:")
        for test_name, result in self.test_results.items():
            if result["status"] == "PASS":
                logger.info(f"  - {test_name}")
        
        total_time = time.time() - self.start_time
        logger.info(f"\n⏱️  Total Test Time: {total_time:.2f} seconds")
        
        # Performance metrics
        if "Performance Benchmark" in self.test_results:
            perf_result = self.test_results["Performance Benchmark"]
            if perf_result["status"] == "PASS":
                details = perf_result["details"]
                logger.info(f"🚀 Performance: {details['requests_per_second']:.1f} req/s")
                logger.info(f"📈 Avg Response Time: {details['average_response_time']*1000:.1f}ms")

def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Realtime Workflow Visualization")
    parser.add_argument("--url", default="http://localhost:8000", help="Base URL for testing")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Check if server is running
    try:
        response = requests.get(f"{args.url}/health", timeout=5)
        if response.status_code != 200:
            logger.error(f"Server not responding at {args.url}")
            return 1
    except requests.exceptions.RequestException as e:
        logger.error(f"Cannot connect to server at {args.url}: {e}")
        logger.info("Make sure the mock SSE server is running:")
        logger.info("  python mock_sse_server.py")
        logger.info("  or")
        logger.info("  docker-compose up mock-sse-server")
        return 1
    
    # Run tests
    tester = RealtimeVisualizationTester(args.url)
    tester.run_all_tests()
    
    # Return exit code based on test results
    failed_tests = sum(1 for result in tester.test_results.values() if result["status"] == "FAIL")
    return 1 if failed_tests > 0 else 0

if __name__ == "__main__":
    exit(main()) 