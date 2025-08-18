#!/usr/bin/env python3
"""
Workflow Events System for Construction Industry Agents
Provides real-time event generation and handling for workflow visualization
"""

import json
import time
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
import logging
from pathlib import Path
import sqlite3
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class EventType(Enum):
    """Workflow event types"""
    WORKFLOW_STARTED = "workflow_started"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_ERROR = "workflow_error"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_ERROR = "agent_error"
    PERFORMANCE_METRIC = "performance_metric"
    PROGRESS_UPDATE = "progress_update"
    STATUS_UPDATE = "status_update"

class EventStatus(Enum):
    """Event status values"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    PROGRESS = "progress"

@dataclass
class WorkflowEvent:
    """Workflow event model"""
    event_id: str
    workflow_id: str
    timestamp: datetime
    event_type: str
    agent_name: str
    status: str
    message: str
    data: Dict[str, Any]
    duration: Optional[float] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        event_dict = asdict(self)
        event_dict['timestamp'] = self.timestamp.isoformat()
        return event_dict

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict())

class EventStorage:
    """Event storage and retrieval system"""
    
    def __init__(self, db_path: str = "workflow_events.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the event database"""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS workflow_events (
                    event_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    agent_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    message TEXT NOT NULL,
                    data TEXT NOT NULL,
                    duration REAL,
                    error TEXT,
                    metadata TEXT
                )
            """)
            
            # Create indexes for better query performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_workflow_id ON workflow_events(workflow_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON workflow_events(timestamp)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_event_type ON workflow_events(event_type)")
    
    @contextmanager
    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()
    
    def store_event(self, event: WorkflowEvent):
        """Store a workflow event"""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO workflow_events 
                    (event_id, workflow_id, timestamp, event_type, agent_name, status, message, data, duration, error, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    event.event_id,
                    event.workflow_id,
                    event.timestamp.isoformat(),
                    event.event_type,
                    event.agent_name,
                    event.status,
                    event.message,
                    json.dumps(event.data),
                    event.duration,
                    event.error,
                    json.dumps(event.metadata) if event.metadata else None
                ))
                conn.commit()
            logger.debug(f"Stored event: {event.event_id}")
        except Exception as e:
            logger.error(f"Failed to store event {event.event_id}: {e}")
            raise
    
    def get_events_by_workflow(self, workflow_id: str, limit: int = 100) -> List[WorkflowEvent]:
        """Get events for a specific workflow"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT event_id, workflow_id, timestamp, event_type, agent_name, status, message, data, duration, error, metadata
                    FROM workflow_events 
                    WHERE workflow_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (workflow_id, limit))
                
                events = []
                for row in cursor.fetchall():
                    event = WorkflowEvent(
                        event_id=row[0],
                        workflow_id=row[1],
                        timestamp=datetime.fromisoformat(row[2]),
                        event_type=row[3],
                        agent_name=row[4],
                        status=row[5],
                        message=row[6],
                        data=json.loads(row[7]),
                        duration=row[8],
                        error=row[9],
                        metadata=json.loads(row[10]) if row[10] else None
                    )
                    events.append(event)
                
                return events
        except Exception as e:
            logger.error(f"Failed to retrieve events for workflow {workflow_id}: {e}")
            return []
    
    def get_recent_events(self, limit: int = 50) -> List[WorkflowEvent]:
        """Get recent events across all workflows"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT event_id, workflow_id, timestamp, event_type, agent_name, status, message, data, duration, error, metadata
                    FROM workflow_events 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (limit,))
                
                events = []
                for row in cursor.fetchall():
                    event = WorkflowEvent(
                        event_id=row[0],
                        workflow_id=row[1],
                        timestamp=datetime.fromisoformat(row[2]),
                        event_type=row[3],
                        agent_name=row[4],
                        status=row[5],
                        message=row[6],
                        data=json.loads(row[7]),
                        duration=row[8],
                        error=row[9],
                        metadata=json.loads(row[10]) if row[10] else None
                    )
                    events.append(event)
                
                return events
        except Exception as e:
            logger.error(f"Failed to retrieve recent events: {e}")
            return []

class EventGenerator:
    """Generate workflow events during execution"""
    
    def __init__(self, workflow_id: str, storage: Optional[EventStorage] = None):
        self.workflow_id = workflow_id
        self.storage = storage or EventStorage()
        self.event_handlers: List[Callable[[WorkflowEvent], None]] = []
        self.start_times: Dict[str, float] = {}
    
    def add_handler(self, handler: Callable[[WorkflowEvent], None]):
        """Add an event handler"""
        self.event_handlers.append(handler)
    
    def _create_event(self, event_type: str, agent_name: str, status: str, message: str, 
                     data: Dict[str, Any] = None, error: str = None, metadata: Dict[str, Any] = None) -> WorkflowEvent:
        """Create a workflow event"""
        event_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # Calculate duration if agent was started
        duration = None
        if agent_name in self.start_times:
            duration = time.time() - self.start_times[agent_name]
            del self.start_times[agent_name]
        
        event = WorkflowEvent(
            event_id=event_id,
            workflow_id=self.workflow_id,
            timestamp=timestamp,
            event_type=event_type,
            agent_name=agent_name,
            status=status,
            message=message,
            data=data or {},
            duration=duration,
            error=error,
            metadata=metadata
        )
        
        return event
    
    def _emit_event(self, event: WorkflowEvent):
        """Emit an event to all handlers and storage"""
        try:
            # Store event
            if self.storage:
                self.storage.store_event(event)
            
            # Notify handlers
            for handler in self.event_handlers:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Event handler failed: {e}")
            
            logger.debug(f"Emitted event: {event.event_type} - {event.message}")
        except Exception as e:
            logger.error(f"Failed to emit event: {e}")
    
    def workflow_started(self, data: Dict[str, Any] = None):
        """Emit workflow started event"""
        event = self._create_event(
            event_type=EventType.WORKFLOW_STARTED.value,
            agent_name="workflow_orchestrator",
            status=EventStatus.INFO.value,
            message="Workflow execution started",
            data=data or {}
        )
        self._emit_event(event)
    
    def workflow_completed(self, data: Dict[str, Any] = None):
        """Emit workflow completed event"""
        event = self._create_event(
            event_type=EventType.WORKFLOW_COMPLETED.value,
            agent_name="workflow_orchestrator",
            status=EventStatus.SUCCESS.value,
            message="Workflow execution completed",
            data=data or {}
        )
        self._emit_event(event)
    
    def workflow_error(self, error: str, data: Dict[str, Any] = None):
        """Emit workflow error event"""
        event = self._create_event(
            event_type=EventType.WORKFLOW_ERROR.value,
            agent_name="workflow_orchestrator",
            status=EventStatus.ERROR.value,
            message="Workflow execution failed",
            data=data or {},
            error=error
        )
        self._emit_event(event)
    
    def agent_started(self, agent_name: str, data: Dict[str, Any] = None):
        """Emit agent started event"""
        self.start_times[agent_name] = time.time()
        event = self._create_event(
            event_type=EventType.AGENT_STARTED.value,
            agent_name=agent_name,
            status=EventStatus.PROGRESS.value,
            message=f"{agent_name} processing started",
            data=data or {}
        )
        self._emit_event(event)
    
    def agent_completed(self, agent_name: str, data: Dict[str, Any] = None):
        """Emit agent completed event"""
        event = self._create_event(
            event_type=EventType.AGENT_COMPLETED.value,
            agent_name=agent_name,
            status=EventStatus.SUCCESS.value,
            message=f"{agent_name} processing completed",
            data=data or {}
        )
        self._emit_event(event)
    
    def agent_error(self, agent_name: str, error: str, data: Dict[str, Any] = None):
        """Emit agent error event"""
        event = self._create_event(
            event_type=EventType.AGENT_ERROR.value,
            agent_name=agent_name,
            status=EventStatus.ERROR.value,
            message=f"{agent_name} processing failed",
            data=data or {},
            error=error
        )
        self._emit_event(event)
    
    def performance_metric(self, agent_name: str, metric_name: str, value: float, unit: str = None):
        """Emit performance metric event"""
        data = {
            "metric_name": metric_name,
            "value": value,
            "unit": unit
        }
        event = self._create_event(
            event_type=EventType.PERFORMANCE_METRIC.value,
            agent_name=agent_name,
            status=EventStatus.INFO.value,
            message=f"Performance metric: {metric_name} = {value}{unit or ''}",
            data=data
        )
        self._emit_event(event)
    
    def progress_update(self, agent_name: str, progress: float, message: str = None):
        """Emit progress update event"""
        data = {"progress": progress}
        event = self._create_event(
            event_type=EventType.PROGRESS_UPDATE.value,
            agent_name=agent_name,
            status=EventStatus.PROGRESS.value,
            message=message or f"Progress: {progress:.1f}%",
            data=data
        )
        self._emit_event(event)
    
    def status_update(self, agent_name: str, status: str, message: str, data: Dict[str, Any] = None):
        """Emit status update event"""
        event = self._create_event(
            event_type=EventType.STATUS_UPDATE.value,
            agent_name=agent_name,
            status=status,
            message=message,
            data=data or {}
        )
        self._emit_event(event)

class EventManager:
    """Global event manager for the system"""
    
    def __init__(self):
        self.storage = EventStorage()
        self.active_generators: Dict[str, EventGenerator] = {}
    
    def create_generator(self, workflow_id: str) -> EventGenerator:
        """Create a new event generator for a workflow"""
        generator = EventGenerator(workflow_id, self.storage)
        self.active_generators[workflow_id] = generator
        return generator
    
    def get_generator(self, workflow_id: str) -> Optional[EventGenerator]:
        """Get an existing event generator"""
        return self.active_generators.get(workflow_id)
    
    def remove_generator(self, workflow_id: str):
        """Remove an event generator"""
        if workflow_id in self.active_generators:
            del self.active_generators[workflow_id]
    
    def get_active_workflows(self) -> List[str]:
        """Get list of active workflow IDs"""
        return list(self.active_generators.keys())
    
    def get_workflow_events(self, workflow_id: str, limit: int = 100) -> List[WorkflowEvent]:
        """Get events for a specific workflow"""
        return self.storage.get_events_by_workflow(workflow_id, limit)
    
    def get_recent_events(self, limit: int = 50) -> List[WorkflowEvent]:
        """Get recent events across all workflows"""
        return self.storage.get_recent_events(limit)

# Global event manager instance
event_manager = EventManager()

if __name__ == "__main__":
    # Test the event system
    print("Testing Workflow Events System...")
    
    # Create a test generator
    generator = event_manager.create_generator("TEST_WORKFLOW_001")
    
    # Add a simple handler
    def print_event(event: WorkflowEvent):
        print(f"[{event.timestamp}] {event.event_type}: {event.message}")
    
    generator.add_handler(print_event)
    
    # Generate some test events
    generator.workflow_started({"test": True})
    generator.agent_started("excel_parser_agent", {"file": "test.xlsx"})
    generator.progress_update("excel_parser_agent", 50.0, "Parsing Excel file...")
    generator.agent_completed("excel_parser_agent", {"items_parsed": 10})
    generator.workflow_completed({"total_items": 10, "success": True})
    
    print("Event system test completed!") 