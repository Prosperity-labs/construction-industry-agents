#!/usr/bin/env python3
"""
Mock SSE Server for Construction Industry Agents
Generates realistic workflow events for testing and development
"""

import json
import time
import random
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import logging
import os

logger = logging.getLogger(__name__)

class MockEventGenerator:
    """Generate realistic mock workflow events"""
    
    def __init__(self):
        self.workflow_id = f"MOCK_WORKFLOW_{int(time.time())}"
        self.agents = [
            "excel_parser_agent",
            "supplier_mapping_agent", 
            "communication_agent",
            "response_parser_agent",
            "quote_calculator_agent",
            "document_generator_agent"
        ]
        self.agent_descriptions = {
            "excel_parser_agent": "Excel Parser Agent",
            "supplier_mapping_agent": "Supplier Mapping Agent",
            "communication_agent": "Communication Agent", 
            "response_parser_agent": "Response Parser Agent",
            "quote_calculator_agent": "Quote Calculator Agent",
            "document_generator_agent": "Document Generator Agent"
        }
        self.event_count = 0
        self.start_time = time.time()
    
    def generate_workflow_started_event(self) -> Dict[str, Any]:
        """Generate workflow started event"""
        return {
            "event_id": f"event_{self.event_count}",
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "workflow_started",
            "agent_name": "workflow_orchestrator",
            "status": "info",
            "message": "Workflow execution started",
            "data": {
                "input_file": "test_construction_spec.xlsx",
                "total_items": random.randint(5, 25),
                "project_type": random.choice(["HVAC", "Electrical", "Plumbing", "General Construction"])
            },
            "duration": None,
            "error": None,
            "metadata": {
                "source": "mock_server",
                "version": "1.0"
            }
        }
    
    def generate_agent_started_event(self, agent_name: str) -> Dict[str, Any]:
        """Generate agent started event"""
        self.event_count += 1
        return {
            "event_id": f"event_{self.event_count}",
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "agent_started",
            "agent_name": agent_name,
            "status": "progress",
            "message": f"{self.agent_descriptions[agent_name]} processing started",
            "data": {
                "agent_type": agent_name,
                "items_to_process": random.randint(3, 15)
            },
            "duration": None,
            "error": None,
            "metadata": {
                "source": "mock_server",
                "version": "1.0"
            }
        }
    
    def generate_progress_update_event(self, agent_name: str, progress: float) -> Dict[str, Any]:
        """Generate progress update event"""
        self.event_count += 1
        messages = [
            f"Processing item {int(progress * 10)} of 10",
            f"Analyzing data... {progress:.0f}% complete",
            f"Validating results... {progress:.0f}% done",
            f"Generating output... {progress:.0f}% finished"
        ]
        
        return {
            "event_id": f"event_{self.event_count}",
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "progress_update",
            "agent_name": agent_name,
            "status": "progress",
            "message": random.choice(messages),
            "data": {
                "progress": progress,
                "items_processed": int(progress * 10),
                "total_items": 10
            },
            "duration": None,
            "error": None,
            "metadata": {
                "source": "mock_server",
                "version": "1.0"
            }
        }
    
    def generate_performance_metric_event(self, agent_name: str) -> Dict[str, Any]:
        """Generate performance metric event"""
        self.event_count += 1
        metrics = [
            ("processing_time", random.uniform(0.5, 3.0), "seconds"),
            ("memory_usage", random.uniform(50, 200), "MB"),
            ("items_processed", random.randint(5, 20), "items"),
            ("accuracy_score", random.uniform(0.95, 0.99), "percentage")
        ]
        
        metric_name, value, unit = random.choice(metrics)
        
        return {
            "event_id": f"event_{self.event_count}",
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "performance_metric",
            "agent_name": agent_name,
            "status": "info",
            "message": f"Performance metric: {metric_name} = {value:.2f}{unit}",
            "data": {
                "metric_name": metric_name,
                "value": value,
                "unit": unit
            },
            "duration": None,
            "error": None,
            "metadata": {
                "source": "mock_server",
                "version": "1.0"
            }
        }
    
    def generate_agent_completed_event(self, agent_name: str) -> Dict[str, Any]:
        """Generate agent completed event"""
        self.event_count += 1
        duration = random.uniform(1.0, 5.0)
        
        completion_messages = {
            "excel_parser_agent": f"Successfully parsed {random.randint(5, 20)} construction items",
            "supplier_mapping_agent": f"Mapped {random.randint(3, 8)} items to suppliers",
            "communication_agent": f"Sent requests to {random.randint(2, 6)} suppliers",
            "response_parser_agent": f"Processed {random.randint(2, 6)} supplier responses",
            "quote_calculator_agent": f"Calculated optimal quotes for {random.randint(5, 15)} items",
            "document_generator_agent": f"Generated professional quote documents"
        }
        
        return {
            "event_id": f"event_{self.event_count}",
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "agent_completed",
            "agent_name": agent_name,
            "status": "success",
            "message": completion_messages.get(agent_name, f"{self.agent_descriptions[agent_name]} completed successfully"),
            "data": {
                "duration": duration,
                "items_processed": random.randint(5, 20),
                "success_rate": random.uniform(0.95, 1.0)
            },
            "duration": duration,
            "error": None,
            "metadata": {
                "source": "mock_server",
                "version": "1.0"
            }
        }
    
    def generate_agent_error_event(self, agent_name: str) -> Dict[str, Any]:
        """Generate agent error event (occasionally)"""
        self.event_count += 1
        
        error_messages = [
            "Invalid data format detected",
            "Network timeout occurred",
            "API rate limit exceeded",
            "Configuration error",
            "Resource allocation failed"
        ]
        
        return {
            "event_id": f"event_{self.event_count}",
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "agent_error",
            "agent_name": agent_name,
            "status": "error",
            "message": f"{self.agent_descriptions[agent_name]} encountered an error",
            "data": {
                "error_type": "processing_error",
                "retry_count": 0
            },
            "duration": None,
            "error": random.choice(error_messages),
            "metadata": {
                "source": "mock_server",
                "version": "1.0"
            }
        }
    
    def generate_workflow_completed_event(self) -> Dict[str, Any]:
        """Generate workflow completed event"""
        self.event_count += 1
        total_duration = time.time() - self.start_time
        
        return {
            "event_id": f"event_{self.event_count}",
            "workflow_id": self.workflow_id,
            "timestamp": datetime.now().isoformat(),
            "event_type": "workflow_completed",
            "agent_name": "workflow_orchestrator",
            "status": "success",
            "message": "Workflow execution completed successfully",
            "data": {
                "total_duration": total_duration,
                "total_items_processed": random.randint(10, 30),
                "quotes_generated": random.randint(1, 3),
                "success_rate": random.uniform(0.95, 1.0)
            },
            "duration": total_duration,
            "error": None,
            "metadata": {
                "source": "mock_server",
                "version": "1.0"
            }
        }

class MockSSEServer:
    """Mock SSE server for testing and development"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.cors = CORS(self.app)
        
        # Event generation
        self.event_generator = MockEventGenerator()
        self.subscribers = set()
        self.running = False
        self.event_thread = None
        
        # Setup routes
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            """Serve the dashboard HTML"""
            return self._get_dashboard_html()
        
        @self.app.route('/events/stream')
        def event_stream():
            """SSE event stream endpoint"""
            return self._handle_sse_stream()
        
        @self.app.route('/events/history')
        def get_event_history():
            """Get historical events (mock)"""
            limit = int(request.args.get('limit', 50))
            events = self._generate_mock_history(limit)
            return jsonify(events)
        
        @self.app.route('/workflows/active')
        def get_active_workflows():
            """Get list of active workflows (mock)"""
            return jsonify({
                "active_workflows": [self.event_generator.workflow_id],
                "count": 1
            })
        
        @self.app.route('/metrics/performance')
        def get_performance_metrics():
            """Get performance metrics (mock)"""
            return jsonify(self._get_mock_metrics())
        
        @self.app.route('/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "subscribers": len(self.subscribers),
                "active_workflows": 1,
                "mock_server": True
            })
        
        @self.app.route('/mock/start-workflow')
        def start_mock_workflow():
            """Start a mock workflow"""
            self._start_mock_workflow()
            return jsonify({"status": "started", "workflow_id": self.event_generator.workflow_id})
    
    def _handle_sse_stream(self):
        """Handle SSE stream connection"""
        def generate():
            client_id = f"mock_client_{int(time.time() * 1000)}"
            self.subscribers.add(client_id)
            logger.info(f"Mock SSE client connected: {client_id}")
            
            try:
                # Send initial connection event
                yield f"data: {json.dumps({'type': 'connection', 'client_id': client_id, 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # Keep connection alive
                while client_id in self.subscribers:
                    try:
                        # Send heartbeat every 30 seconds
                        yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': datetime.now().isoformat()})}\n\n"
                        time.sleep(30)
                    except Exception as e:
                        logger.error(f"Error in mock SSE stream for {client_id}: {e}")
                        break
                        
            except GeneratorExit:
                logger.info(f"Mock SSE client disconnected: {client_id}")
            finally:
                if client_id in self.subscribers:
                    self.subscribers.remove(client_id)
        
        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Cache-Control'
            }
        )
    
    def _get_dashboard_html(self):
        """Get the dashboard HTML with mock controls"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mock SSE Server - Construction Industry Agents</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2em;
        }
        .content {
            padding: 20px;
        }
        .mock-controls {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
        }
        .mock-controls h3 {
            margin: 0 0 15px 0;
            color: #856404;
        }
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-right: 10px;
            font-size: 14px;
        }
        .btn:hover {
            background: #5a6fd8;
        }
        .btn-danger {
            background: #e74c3c;
        }
        .btn-danger:hover {
            background: #c0392b;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .metric-card h3 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .events-section {
            margin-top: 20px;
        }
        .event-list {
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #e9ecef;
            border-radius: 8px;
        }
        .event-item {
            padding: 10px 15px;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .event-item:last-child {
            border-bottom: none;
        }
        .event-info {
            flex: 1;
        }
        .event-time {
            font-size: 0.8em;
            color: #6c757d;
        }
        .event-message {
            font-weight: 500;
            color: #333;
        }
        .event-agent {
            font-size: 0.9em;
            color: #667eea;
        }
        .event-status {
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.7em;
            font-weight: bold;
        }
        .status-success { background: #d4edda; color: #155724; }
        .status-error { background: #f8d7da; color: #721c24; }
        .status-progress { background: #fff3cd; color: #856404; }
        .status-info { background: #d1ecf1; color: #0c5460; }
        .loading {
            text-align: center;
            padding: 40px;
            color: #6c757d;
        }
        .mock-badge {
            background: #ff6b6b;
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7em;
            font-weight: bold;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗️ Construction Industry Agents <span class="mock-badge">MOCK</span></h1>
            <p>Mock SSE Server for Testing and Development</p>
        </div>
        
        <div class="content">
            <div class="mock-controls">
                <h3>🎮 Mock Controls</h3>
                <button class="btn" onclick="startMockWorkflow()">Start Mock Workflow</button>
                <button class="btn" onclick="generateRandomEvent()">Generate Random Event</button>
                <button class="btn btn-danger" onclick="clearEvents()">Clear Events</button>
                <button class="btn" onclick="toggleAutoMode()" id="auto-btn">Enable Auto Mode</button>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-card">
                    <h3>Mock Workflows</h3>
                    <div class="metric-value" id="mock-workflows">1</div>
                </div>
                <div class="metric-card">
                    <h3>Connected Clients</h3>
                    <div class="metric-value" id="connected-clients">-</div>
                </div>
                <div class="metric-card">
                    <h3>Events Generated</h3>
                    <div class="metric-value" id="events-generated">0</div>
                </div>
                <div class="metric-card">
                    <h3>Server Status</h3>
                    <div class="metric-value" id="server-status">Running</div>
                </div>
            </div>
            
            <div class="events-section">
                <h2>Mock Events <span class="mock-badge">LIVE</span></h2>
                <div id="events-container" class="event-list">
                    <div class="loading">Waiting for mock events...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        class MockDashboard {
            constructor() {
                this.eventSource = null;
                this.connected = false;
                this.autoMode = false;
                this.eventCount = 0;
                this.init();
            }
            
            init() {
                this.connectSSE();
                this.loadInitialData();
                this.startPeriodicUpdates();
            }
            
            connectSSE() {
                try {
                    this.eventSource = new EventSource('/events/stream');
                    
                    this.eventSource.onopen = () => {
                        console.log('Mock SSE connection established');
                        this.connected = true;
                        this.updateServerStatus('Connected');
                    };
                    
                    this.eventSource.onmessage = (event) => {
                        const data = JSON.parse(event.data);
                        this.handleEvent(data);
                    };
                    
                    this.eventSource.onerror = (error) => {
                        console.error('Mock SSE connection error:', error);
                        this.connected = false;
                        this.updateServerStatus('Disconnected');
                        this.reconnect();
                    };
                } catch (error) {
                    console.error('Failed to connect to mock SSE:', error);
                    this.updateServerStatus('Error');
                }
            }
            
            reconnect() {
                setTimeout(() => {
                    console.log('Attempting to reconnect to mock server...');
                    this.connectSSE();
                }, 5000);
            }
            
            async loadInitialData() {
                try {
                    await Promise.all([
                        this.loadMetrics()
                    ]);
                } catch (error) {
                    console.error('Failed to load initial data:', error);
                }
            }
            
            async loadMetrics() {
                try {
                    const response = await fetch('/health');
                    const data = await response.json();
                    this.updateMetrics(data);
                } catch (error) {
                    console.error('Failed to load metrics:', error);
                }
            }
            
            updateMetrics(data) {
                document.getElementById('connected-clients').textContent = data.subscribers || 0;
                document.getElementById('events-generated').textContent = this.eventCount;
            }
            
            updateServerStatus(status) {
                const element = document.getElementById('server-status');
                element.textContent = status;
            }
            
            handleEvent(data) {
                if (data.type === 'workflow_event') {
                    this.addEventToList(data.event);
                    this.eventCount++;
                    this.updateMetrics({});
                }
            }
            
            addEventToList(event) {
                const container = document.getElementById('events-container');
                
                // Remove loading message if present
                if (container.querySelector('.loading')) {
                    container.innerHTML = '';
                }
                
                const eventHtml = `
                    <div class="event-item">
                        <div class="event-info">
                            <div class="event-time">${new Date(event.timestamp).toLocaleTimeString()}</div>
                            <div class="event-message">${event.message}</div>
                            <div class="event-agent">${event.agent_name}</div>
                        </div>
                        <span class="event-status status-${event.status}">${event.status}</span>
                    </div>
                `;
                
                container.insertAdjacentHTML('afterbegin', eventHtml);
                
                // Keep only last 50 events
                const events = container.children;
                if (events.length > 50) {
                    events[events.length - 1].remove();
                }
            }
            
            startPeriodicUpdates() {
                setInterval(() => {
                    this.loadMetrics();
                }, 5000);
            }
            
            async startMockWorkflow() {
                try {
                    const response = await fetch('/mock/start-workflow');
                    const data = await response.json();
                    console.log('Mock workflow started:', data);
                } catch (error) {
                    console.error('Failed to start mock workflow:', error);
                }
            }
            
            async generateRandomEvent() {
                // This would trigger a random event generation
                console.log('Generating random event...');
            }
            
            clearEvents() {
                const container = document.getElementById('events-container');
                container.innerHTML = '<div class="loading">Events cleared...</div>';
                this.eventCount = 0;
                this.updateMetrics({});
            }
            
            toggleAutoMode() {
                this.autoMode = !this.autoMode;
                const btn = document.getElementById('auto-btn');
                btn.textContent = this.autoMode ? 'Disable Auto Mode' : 'Enable Auto Mode';
                btn.className = this.autoMode ? 'btn btn-danger' : 'btn';
                console.log('Auto mode:', this.autoMode ? 'enabled' : 'disabled');
            }
        }
        
        // Global functions for buttons
        window.startMockWorkflow = function() {
            dashboard.startMockWorkflow();
        };
        
        window.generateRandomEvent = function() {
            dashboard.generateRandomEvent();
        };
        
        window.clearEvents = function() {
            dashboard.clearEvents();
        };
        
        window.toggleAutoMode = function() {
            dashboard.toggleAutoMode();
        };
        
        // Initialize dashboard when page loads
        let dashboard;
        document.addEventListener('DOMContentLoaded', () => {
            dashboard = new MockDashboard();
        });
    </script>
</body>
</html>
        """
    
    def _generate_mock_history(self, limit: int) -> List[Dict[str, Any]]:
        """Generate mock historical events"""
        events = []
        for i in range(limit):
            event = {
                "event_id": f"mock_event_{i}",
                "workflow_id": self.event_generator.workflow_id,
                "timestamp": (datetime.now() - timedelta(minutes=i)).isoformat(),
                "event_type": random.choice(["agent_started", "agent_completed", "progress_update"]),
                "agent_name": random.choice(self.event_generator.agents),
                "status": random.choice(["success", "progress", "info"]),
                "message": f"Mock event {i}",
                "data": {"mock": True},
                "duration": random.uniform(0.1, 2.0),
                "error": None,
                "metadata": {"source": "mock_server"}
            }
            events.append(event)
        return events
    
    def _get_mock_metrics(self) -> Dict[str, Any]:
        """Get mock performance metrics"""
        return {
            "active_workflows": 1,
            "connected_clients": len(self.subscribers),
            "recent_events_count": self.event_generator.event_count,
            "system_uptime": time.time(),
            "timestamp": datetime.now().isoformat(),
            "mock_server": True
        }
    
    def _start_mock_workflow(self):
        """Start a mock workflow simulation"""
        if self.running:
            return
        
        self.running = True
        self.event_thread = threading.Thread(target=self._run_mock_workflow, daemon=True)
        self.event_thread.start()
        logger.info("Mock workflow started")
    
    def _run_mock_workflow(self):
        """Run the mock workflow simulation"""
        try:
            # Workflow started
            self._broadcast_event(self.event_generator.generate_workflow_started_event())
            time.sleep(1)
            
            # Process each agent
            for agent in self.event_generator.agents:
                # Agent started
                self._broadcast_event(self.event_generator.generate_agent_started_event(agent))
                time.sleep(0.5)
                
                # Progress updates
                for progress in [25, 50, 75, 100]:
                    self._broadcast_event(self.event_generator.generate_progress_update_event(agent, progress))
                    time.sleep(random.uniform(0.5, 1.5))
                
                # Performance metric
                self._broadcast_event(self.event_generator.generate_performance_metric_event(agent))
                time.sleep(0.5)
                
                # Agent completed (with occasional error)
                if random.random() < 0.1:  # 10% chance of error
                    self._broadcast_event(self.event_generator.generate_agent_error_event(agent))
                else:
                    self._broadcast_event(self.event_generator.generate_agent_completed_event(agent))
                
                time.sleep(1)
            
            # Workflow completed
            self._broadcast_event(self.event_generator.generate_workflow_completed_event())
            
        except Exception as e:
            logger.error(f"Error in mock workflow: {e}")
        finally:
            self.running = False
            logger.info("Mock workflow completed")
    
    def _broadcast_event(self, event: Dict[str, Any]):
        """Broadcast event to all subscribers"""
        if not self.subscribers:
            return
        
        event_data = {
            "type": "workflow_event",
            "event": event,
            "timestamp": datetime.now().isoformat()
        }
        
        # Log the event
        logger.info(f"Broadcasting mock event: {event['event_type']} - {event['message']}")
        
        # In a real implementation, this would send to actual SSE clients
        # For now, we'll just log the event
    
    def run(self, debug: bool = False):
        """Run the mock SSE server"""
        logger.info(f"Starting Mock SSE server on {self.host}:{self.port}")
        
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=debug,
                threaded=True
            )
        except KeyboardInterrupt:
            logger.info("Shutting down Mock SSE server...")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get configuration from environment variables
    host = os.getenv('MOCK_SSE_HOST', '0.0.0.0')
    port = int(os.getenv('MOCK_SSE_PORT', '8000'))
    
    # Create and run server
    server = MockSSEServer(host, port)
    server.run(debug=True) 