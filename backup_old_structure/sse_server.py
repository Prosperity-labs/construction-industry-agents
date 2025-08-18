#!/usr/bin/env python3
"""
SSE Server for Construction Industry Agents
Provides real-time Server-Sent Events streaming for workflow visualization
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Set, Optional, Any
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
import logging
from queue import Queue
import os

from workflow_events import WorkflowEvent, EventManager, event_manager

logger = logging.getLogger(__name__)

class SSEServer:
    """Server-Sent Events server for real-time workflow monitoring"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.cors = CORS(self.app)
        
        # Event broadcasting
        self.subscribers: Set[str] = set()
        self.event_queue = Queue()
        self.broadcast_thread = None
        self.running = False
        
        # Setup routes
        self._setup_routes()
        
        # Connect to event manager
        self.event_manager = event_manager
    
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
            """Get historical events"""
            workflow_id = request.args.get('workflow_id')
            limit = int(request.args.get('limit', 50))
            
            if workflow_id:
                events = self.event_manager.get_workflow_events(workflow_id, limit)
            else:
                events = self.event_manager.get_recent_events(limit)
            
            return jsonify([event.to_dict() for event in events])
        
        @self.app.route('/workflows/active')
        def get_active_workflows():
            """Get list of active workflows"""
            workflows = self.event_manager.get_active_workflows()
            return jsonify({
                "active_workflows": workflows,
                "count": len(workflows)
            })
        
        @self.app.route('/metrics/performance')
        def get_performance_metrics():
            """Get performance metrics"""
            return jsonify(self._get_performance_metrics())
        
        @self.app.route('/health')
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "subscribers": len(self.subscribers),
                "active_workflows": len(self.event_manager.get_active_workflows())
            })
    
    def _handle_sse_stream(self):
        """Handle SSE stream connection"""
        def generate():
            # Add client to subscribers
            client_id = f"client_{int(time.time() * 1000)}"
            self.subscribers.add(client_id)
            logger.info(f"New SSE client connected: {client_id}")
            
            try:
                # Send initial connection event
                yield f"data: {json.dumps({'type': 'connection', 'client_id': client_id, 'timestamp': datetime.now().isoformat()})}\n\n"
                
                # Keep connection alive and stream events
                while client_id in self.subscribers:
                    try:
                        # Send heartbeat every 30 seconds
                        yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': datetime.now().isoformat()})}\n\n"
                        time.sleep(30)
                    except Exception as e:
                        logger.error(f"Error in SSE stream for {client_id}: {e}")
                        break
                        
            except GeneratorExit:
                logger.info(f"SSE client disconnected: {client_id}")
            finally:
                # Remove client from subscribers
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
        """Get the dashboard HTML"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Construction Industry Agents - Real-time Dashboard</title>
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        .workflow-section {
            margin-bottom: 30px;
        }
        .workflow-list {
            display: grid;
            gap: 15px;
        }
        .workflow-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }
        .workflow-header {
            display: flex;
            justify-content: between;
            align-items: center;
            margin-bottom: 10px;
        }
        .workflow-id {
            font-weight: bold;
            color: #333;
        }
        .workflow-status {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .status-active { background: #d4edda; color: #155724; }
        .status-completed { background: #cce5ff; color: #004085; }
        .status-error { background: #f8d7da; color: #721c24; }
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
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏗️ Construction Industry Agents</h1>
            <p>Real-time Workflow Visualization Dashboard</p>
        </div>
        
        <div class="content">
            <div class="metrics-grid">
                <div class="metric-card">
                    <h3>Active Workflows</h3>
                    <div class="metric-value" id="active-workflows">-</div>
                </div>
                <div class="metric-card">
                    <h3>Connected Clients</h3>
                    <div class="metric-value" id="connected-clients">-</div>
                </div>
                <div class="metric-card">
                    <h3>Total Events</h3>
                    <div class="metric-value" id="total-events">-</div>
                </div>
                <div class="metric-card">
                    <h3>System Status</h3>
                    <div class="metric-value" id="system-status">-</div>
                </div>
            </div>
            
            <div class="workflow-section">
                <h2>Active Workflows</h2>
                <div id="workflows-container" class="workflow-list">
                    <div class="loading">Loading workflows...</div>
                </div>
            </div>
            
            <div class="events-section">
                <h2>Recent Events</h2>
                <div id="events-container" class="event-list">
                    <div class="loading">Loading events...</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        class WorkflowDashboard {
            constructor() {
                this.eventSource = null;
                this.connected = false;
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
                        console.log('SSE connection established');
                        this.connected = true;
                        this.updateSystemStatus('Connected');
                    };
                    
                    this.eventSource.onmessage = (event) => {
                        const data = JSON.parse(event.data);
                        this.handleEvent(data);
                    };
                    
                    this.eventSource.onerror = (error) => {
                        console.error('SSE connection error:', error);
                        this.connected = false;
                        this.updateSystemStatus('Disconnected');
                        this.reconnect();
                    };
                } catch (error) {
                    console.error('Failed to connect to SSE:', error);
                    this.updateSystemStatus('Error');
                }
            }
            
            reconnect() {
                setTimeout(() => {
                    console.log('Attempting to reconnect...');
                    this.connectSSE();
                }, 5000);
            }
            
            async loadInitialData() {
                try {
                    await Promise.all([
                        this.loadActiveWorkflows(),
                        this.loadRecentEvents(),
                        this.loadMetrics()
                    ]);
                } catch (error) {
                    console.error('Failed to load initial data:', error);
                }
            }
            
            async loadActiveWorkflows() {
                try {
                    const response = await fetch('/workflows/active');
                    const data = await response.json();
                    this.updateWorkflows(data.active_workflows);
                } catch (error) {
                    console.error('Failed to load workflows:', error);
                }
            }
            
            async loadRecentEvents() {
                try {
                    const response = await fetch('/events/history?limit=20');
                    const events = await response.json();
                    this.updateEvents(events);
                } catch (error) {
                    console.error('Failed to load events:', error);
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
            
            updateWorkflows(workflows) {
                const container = document.getElementById('workflows-container');
                
                if (workflows.length === 0) {
                    container.innerHTML = '<div class="loading">No active workflows</div>';
                    return;
                }
                
                container.innerHTML = workflows.map(workflow => `
                    <div class="workflow-card">
                        <div class="workflow-header">
                            <span class="workflow-id">${workflow}</span>
                            <span class="workflow-status status-active">Active</span>
                        </div>
                        <div class="workflow-info">
                            <small>Started: ${new Date().toLocaleTimeString()}</small>
                        </div>
                    </div>
                `).join('');
            }
            
            updateEvents(events) {
                const container = document.getElementById('events-container');
                
                if (events.length === 0) {
                    container.innerHTML = '<div class="loading">No events available</div>';
                    return;
                }
                
                container.innerHTML = events.map(event => `
                    <div class="event-item">
                        <div class="event-info">
                            <div class="event-time">${new Date(event.timestamp).toLocaleTimeString()}</div>
                            <div class="event-message">${event.message}</div>
                            <div class="event-agent">${event.agent_name}</div>
                        </div>
                        <span class="event-status status-${event.status}">${event.status}</span>
                    </div>
                `).join('');
            }
            
            updateMetrics(data) {
                document.getElementById('active-workflows').textContent = data.active_workflows || 0;
                document.getElementById('connected-clients').textContent = data.subscribers || 0;
                document.getElementById('total-events').textContent = '-'; // Would need additional endpoint
            }
            
            updateSystemStatus(status) {
                const element = document.getElementById('system-status');
                element.textContent = status;
                element.className = `metric-value status-${status.toLowerCase()}`;
            }
            
            handleEvent(data) {
                // Handle real-time events
                if (data.type === 'workflow_event') {
                    this.addEventToList(data.event);
                } else if (data.type === 'workflow_update') {
                    this.updateWorkflowStatus(data.workflow_id, data.status);
                }
            }
            
            addEventToList(event) {
                const container = document.getElementById('events-container');
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
                }, 10000); // Update every 10 seconds
            }
        }
        
        // Initialize dashboard when page loads
        document.addEventListener('DOMContentLoaded', () => {
            new WorkflowDashboard();
        });
    </script>
</body>
</html>
        """
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        active_workflows = self.event_manager.get_active_workflows()
        recent_events = self.event_manager.get_recent_events(10)
        
        return {
            "active_workflows": len(active_workflows),
            "connected_clients": len(self.subscribers),
            "recent_events_count": len(recent_events),
            "system_uptime": time.time(),
            "timestamp": datetime.now().isoformat()
        }
    
    def broadcast_event(self, event: WorkflowEvent):
        """Broadcast event to all connected clients"""
        if not self.subscribers:
            return
        
        event_data = {
            "type": "workflow_event",
            "event": event.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
        
        # Add to queue for broadcasting
        self.event_queue.put(event_data)
    
    def start_broadcasting(self):
        """Start the event broadcasting thread"""
        if self.broadcast_thread and self.broadcast_thread.is_alive():
            return
        
        self.running = True
        self.broadcast_thread = threading.Thread(target=self._broadcast_loop, daemon=True)
        self.broadcast_thread.start()
        logger.info("Event broadcasting started")
    
    def stop_broadcasting(self):
        """Stop the event broadcasting thread"""
        self.running = False
        if self.broadcast_thread:
            self.broadcast_thread.join(timeout=5)
        logger.info("Event broadcasting stopped")
    
    def _broadcast_loop(self):
        """Main broadcasting loop"""
        while self.running:
            try:
                # Process events from queue
                while not self.event_queue.empty():
                    event_data = self.event_queue.get_nowait()
                    self._send_to_subscribers(event_data)
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
            except Exception as e:
                logger.error(f"Error in broadcast loop: {e}")
                time.sleep(1)
    
    def _send_to_subscribers(self, event_data: Dict[str, Any]):
        """Send event data to all subscribers"""
        # In a real implementation, this would send to actual SSE clients
        # For now, we'll just log the event
        logger.info(f"Broadcasting event: {event_data}")
    
    def run(self, debug: bool = False):
        """Run the SSE server"""
        logger.info(f"Starting SSE server on {self.host}:{self.port}")
        self.start_broadcasting()
        
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=debug,
                threaded=True
            )
        except KeyboardInterrupt:
            logger.info("Shutting down SSE server...")
        finally:
            self.stop_broadcasting()

def create_sse_server(host: str = "0.0.0.0", port: int = 8000) -> SSEServer:
    """Create and configure SSE server"""
    server = SSEServer(host, port)
    
    # Add event handler to broadcast events
    def broadcast_handler(event: WorkflowEvent):
        server.broadcast_event(event)
    
    # Register with global event manager
    event_manager.storage.event_handlers.append(broadcast_handler)
    
    return server

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create and run server
    server = create_sse_server()
    server.run(debug=True) 