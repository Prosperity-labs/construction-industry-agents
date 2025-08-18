# Derived Prompts - Construction Industry Agents

## Overview

This document provides comprehensive prompts and instructions for working with the Construction Industry Agents system. These prompts are derived from the system architecture and can be used for development, testing, maintenance, and operational tasks.

## Development Prompts

### System Architecture Analysis

#### Prompt 1: Analyze System Components
```
Analyze the Construction Industry Agents system architecture and provide:

1. **Component Overview**: List all 6 agents and their primary responsibilities
2. **Data Flow**: Describe how data flows between agents
3. **Dependencies**: Identify inter-agent dependencies and external dependencies
4. **Integration Points**: Map out where agents connect to external services
5. **Error Handling**: Identify error handling patterns across the system

Focus on:
- Modular design principles
- Loose coupling between agents
- Data transformation patterns
- Error recovery mechanisms
- Performance optimization opportunities

Provide specific code examples where relevant.
```

#### Prompt 2: Code Quality Assessment
```
Perform a comprehensive code quality assessment of the Construction Industry Agents system:

**Scope**: All Python files in the repository
**Focus Areas**:
- Code structure and organization
- Error handling patterns
- Performance optimization
- Security considerations
- Documentation quality
- Testing coverage

**Deliverables**:
1. **Quality Score**: Overall code quality rating (1-10)
2. **Strengths**: List of well-implemented features
3. **Weaknesses**: Areas needing improvement
4. **Recommendations**: Specific actionable improvements
5. **Risk Assessment**: Code-related risks and mitigation strategies

Include specific code examples and suggest refactoring where appropriate.
```

### Agent Development

#### Prompt 3: Create New Agent
```
Create a new agent for the Construction Industry Agents system following the established patterns:

**Requirements**:
- Agent Name: [SPECIFY_AGENT_NAME]
- Purpose: [SPECIFY_PURPOSE]
- Input: [SPECIFY_INPUT_FORMAT]
- Output: [SPECIFY_OUTPUT_FORMAT]
- Dependencies: [SPECIFY_DEPENDENCIES]

**Implementation Requirements**:
1. Follow the standard agent architecture pattern
2. Include comprehensive error handling
3. Implement logging with appropriate levels
4. Add input/output validation
5. Include unit tests
6. Follow the existing code style and conventions
7. Add type hints throughout
8. Include docstrings for all methods

**Template Structure**:
```python
#!/usr/bin/env python3
"""
[AGENT_NAME] for Construction Industry Agents
[DESCRIPTION]
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class [OutputDataClass]:
    """Output data structure"""
    # Define output fields

class [AgentName]:
    """[Agent description]"""
    
    def __init__(self, config: Dict = None):
        """Initialize agent"""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
    
    def process(self, input_data: Any) -> [OutputDataClass]:
        """Main processing method"""
        try:
            # Implementation
            pass
        except Exception as e:
            self.logger.error(f"Processing failed: {e}")
            return self._handle_error(e, input_data)
    
    def _validate_input(self, data: Any) -> Any:
        """Input validation"""
        pass
    
    def _process_data(self, data: Any) -> [OutputDataClass]:
        """Core processing logic"""
        pass
    
    def _validate_output(self, data: [OutputDataClass]) -> [OutputDataClass]:
        """Output validation"""
        pass
    
    def _handle_error(self, error: Exception, input_data: Any) -> [OutputDataClass]:
        """Error handling"""
        pass

if __name__ == "__main__":
    # Test implementation
    pass
```

Provide the complete implementation following these specifications.
```

#### Prompt 4: Enhance Existing Agent
```
Enhance the [AGENT_NAME] agent with the following improvements:

**Current State**: [DESCRIBE_CURRENT_FUNCTIONALITY]
**Enhancement Requirements**:
1. [SPECIFIC_ENHANCEMENT_1]
2. [SPECIFIC_ENHANCEMENT_2]
3. [SPECIFIC_ENHANCEMENT_3]

**Technical Requirements**:
- Maintain backward compatibility
- Add comprehensive error handling
- Implement performance optimizations
- Add new configuration options
- Enhance logging and monitoring
- Update tests to cover new functionality

**Implementation Guidelines**:
- Follow existing code patterns
- Add type hints for new methods
- Include docstrings for all changes
- Update related documentation
- Ensure all tests pass

Provide the enhanced implementation with detailed explanations of changes.
```

### Testing Prompts

#### Prompt 5: Create Comprehensive Test Suite
```
Create a comprehensive test suite for the [AGENT_NAME] agent:

**Test Requirements**:
1. **Unit Tests**: Test individual methods and functions
2. **Integration Tests**: Test agent interactions
3. **Error Handling Tests**: Test error scenarios and edge cases
4. **Performance Tests**: Test processing speed and resource usage
5. **Data Validation Tests**: Test input/output validation

**Test Data Requirements**:
- Valid input data samples
- Invalid input data samples
- Edge case scenarios
- Large dataset samples
- Error condition samples

**Implementation Guidelines**:
```python
import pytest
from unittest.mock import Mock, patch
from [agent_module] import [AgentClass]

class Test[AgentClass]:
    """Test suite for [AgentClass]"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.agent = [AgentClass]()
        self.sample_data = self._load_sample_data()
    
    def test_valid_input_processing(self):
        """Test processing with valid input"""
        # Implementation
    
    def test_invalid_input_handling(self):
        """Test handling of invalid input"""
        # Implementation
    
    def test_error_scenarios(self):
        """Test various error scenarios"""
        # Implementation
    
    def test_performance_benchmarks(self):
        """Test performance under various loads"""
        # Implementation
    
    def _load_sample_data(self):
        """Load test data samples"""
        # Implementation
```

Provide complete test implementation with comprehensive coverage.
```

#### Prompt 6: Performance Testing
```
Create performance tests for the Construction Industry Agents system:

**Performance Metrics to Test**:
1. **Processing Speed**: Time per item and total workflow time
2. **Memory Usage**: Memory consumption during processing
3. **API Efficiency**: OpenAI API call optimization
4. **Scalability**: Performance with different data sizes
5. **Concurrent Processing**: Multi-threading performance

**Test Scenarios**:
- Small projects (1-10 items)
- Medium projects (11-50 items)
- Large projects (50+ items)
- Concurrent processing
- Memory-intensive operations
- Network latency simulation

**Implementation Requirements**:
```python
import time
import psutil
import threading
from concurrent.futures import ThreadPoolExecutor

class PerformanceTestSuite:
    """Performance testing suite"""
    
    def test_processing_speed(self):
        """Test processing speed with various data sizes"""
        # Implementation
    
    def test_memory_usage(self):
        """Test memory consumption patterns"""
        # Implementation
    
    def test_api_efficiency(self):
        """Test OpenAI API usage optimization"""
        # Implementation
    
    def test_concurrent_processing(self):
        """Test concurrent processing capabilities"""
        # Implementation
    
    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        # Implementation
```

Provide complete performance testing implementation with benchmarking and reporting.
```

## Operational Prompts

### System Monitoring

#### Prompt 7: Create Monitoring Dashboard
```
Create a comprehensive monitoring dashboard for the Construction Industry Agents system:

**Monitoring Requirements**:
1. **System Health**: Agent status, API connectivity, resource usage
2. **Performance Metrics**: Processing times, success rates, error rates
3. **Business Metrics**: Quotes generated, cost per quote, customer satisfaction
4. **Security Monitoring**: Access logs, API usage, security events
5. **Resource Monitoring**: CPU, memory, disk, network usage

**Implementation Requirements**:
```python
import psutil
import time
import json
from datetime import datetime
from typing import Dict, List

class SystemMonitor:
    """System monitoring and alerting"""
    
    def __init__(self):
        self.metrics = {}
        self.alerts = []
    
    def collect_system_metrics(self):
        """Collect system performance metrics"""
        # Implementation
    
    def collect_business_metrics(self):
        """Collect business performance metrics"""
        # Implementation
    
    def check_agent_health(self):
        """Check health of all agents"""
        # Implementation
    
    def generate_dashboard_data(self):
        """Generate dashboard data"""
        # Implementation
    
    def send_alerts(self, threshold_violations):
        """Send alerts for threshold violations"""
        # Implementation
```

Provide complete monitoring implementation with real-time metrics and alerting.
```

#### Prompt 8: Create Logging Framework
```
Create a comprehensive logging framework for the Construction Industry Agents system:

**Logging Requirements**:
1. **Structured Logging**: JSON format with consistent fields
2. **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
3. **Context Information**: Workflow ID, agent name, processing step
4. **Performance Logging**: Processing times, resource usage
5. **Error Logging**: Detailed error information with stack traces
6. **Audit Logging**: Security-relevant events and user actions

**Implementation Requirements**:
```python
import logging
import json
import time
from datetime import datetime
from typing import Dict, Any
from functools import wraps

class StructuredLogger:
    """Structured logging with context"""
    
    def __init__(self, name: str, workflow_id: str = None):
        self.logger = logging.getLogger(name)
        self.workflow_id = workflow_id
        self.context = {}
    
    def log_event(self, level: str, message: str, **kwargs):
        """Log structured event"""
        # Implementation
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics"""
        # Implementation
    
    def log_error(self, error: Exception, context: Dict = None):
        """Log error with context"""
        # Implementation
    
    def set_context(self, **kwargs):
        """Set logging context"""
        # Implementation

def log_performance(func):
    """Decorator to log function performance"""
    # Implementation
```

Provide complete logging implementation with structured output and performance tracking.
```

### Troubleshooting Prompts

#### Prompt 9: Create Diagnostic Tools
```
Create diagnostic tools for troubleshooting the Construction Industry Agents system:

**Diagnostic Requirements**:
1. **System Diagnostics**: Check all system components and dependencies
2. **Data Validation**: Validate input data and processing results
3. **Performance Analysis**: Analyze performance bottlenecks
4. **Error Analysis**: Analyze error patterns and root causes
5. **Configuration Validation**: Validate system configuration

**Implementation Requirements**:
```python
import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any

class SystemDiagnostics:
    """System diagnostic tools"""
    
    def __init__(self):
        self.results = {}
    
    def run_full_diagnostics(self):
        """Run complete system diagnostics"""
        # Implementation
    
    def check_system_health(self):
        """Check overall system health"""
        # Implementation
    
    def validate_data_integrity(self):
        """Validate data integrity across the system"""
        # Implementation
    
    def analyze_performance(self):
        """Analyze system performance"""
        # Implementation
    
    def analyze_errors(self):
        """Analyze error patterns"""
        # Implementation
    
    def generate_diagnostic_report(self):
        """Generate comprehensive diagnostic report"""
        # Implementation
```

Provide complete diagnostic implementation with detailed analysis and reporting.
```

#### Prompt 10: Create Recovery Procedures
```
Create automated recovery procedures for the Construction Industry Agents system:

**Recovery Scenarios**:
1. **API Failure Recovery**: Handle OpenAI API outages
2. **Data Corruption Recovery**: Recover from corrupted data
3. **System Crash Recovery**: Recover from system crashes
4. **Network Failure Recovery**: Handle network connectivity issues
5. **Configuration Error Recovery**: Recover from configuration errors

**Implementation Requirements**:
```python
import time
import json
import subprocess
from typing import Dict, List, Any
from pathlib import Path

class RecoveryManager:
    """Automated recovery procedures"""
    
    def __init__(self):
        self.recovery_procedures = {}
        self.backup_locations = {}
    
    def handle_api_failure(self):
        """Handle OpenAI API failure"""
        # Implementation
    
    def handle_data_corruption(self):
        """Handle data corruption"""
        # Implementation
    
    def handle_system_crash(self):
        """Handle system crash recovery"""
        # Implementation
    
    def handle_network_failure(self):
        """Handle network connectivity issues"""
        # Implementation
    
    def handle_configuration_error(self):
        """Handle configuration errors"""
        # Implementation
    
    def execute_recovery_plan(self, failure_type: str):
        """Execute appropriate recovery plan"""
        # Implementation
```

Provide complete recovery implementation with automated procedures and manual fallbacks.
```

## Configuration Prompts

### System Configuration

#### Prompt 11: Create Configuration Management
```
Create a comprehensive configuration management system for the Construction Industry Agents:

**Configuration Requirements**:
1. **Environment-based Configuration**: Development, testing, production
2. **Agent-specific Configuration**: Individual agent settings
3. **API Configuration**: OpenAI API settings and limits
4. **Performance Configuration**: Batch sizes, timeouts, retry settings
5. **Security Configuration**: Access controls, encryption settings
6. **Monitoring Configuration**: Logging levels, alert thresholds

**Implementation Requirements**:
```python
import os
import json
from typing import Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AgentConfig:
    """Agent-specific configuration"""
    name: str
    enabled: bool
    timeout: int
    retry_count: int
    batch_size: int

@dataclass
class APIConfig:
    """API configuration"""
    api_key: str
    base_url: str
    timeout: int
    rate_limit: int
    retry_delay: float

@dataclass
class SystemConfig:
    """System-wide configuration"""
    environment: str
    log_level: str
    output_directory: str
    backup_enabled: bool
    monitoring_enabled: bool

class ConfigurationManager:
    """Configuration management system"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or "config.json"
        self.config = self._load_configuration()
    
    def _load_configuration(self):
        """Load configuration from file"""
        # Implementation
    
    def get_agent_config(self, agent_name: str) -> AgentConfig:
        """Get agent-specific configuration"""
        # Implementation
    
    def get_api_config(self) -> APIConfig:
        """Get API configuration"""
        # Implementation
    
    def get_system_config(self) -> SystemConfig:
        """Get system configuration"""
        # Implementation
    
    def validate_configuration(self):
        """Validate configuration settings"""
        # Implementation
    
    def update_configuration(self, updates: Dict[str, Any]):
        """Update configuration settings"""
        # Implementation
```

Provide complete configuration management implementation with validation and environment support.
```

### Deployment Prompts

#### Prompt 12: Create Deployment Scripts
```
Create deployment scripts for the Construction Industry Agents system:

**Deployment Requirements**:
1. **Environment Setup**: Python environment, dependencies, configuration
2. **Database Setup**: Supplier database initialization
3. **Service Configuration**: System services and monitoring
4. **Security Setup**: API keys, access controls, encryption
5. **Testing**: Post-deployment testing and validation
6. **Rollback**: Deployment rollback procedures

**Implementation Requirements**:
```bash
#!/bin/bash
# deployment.sh - Deployment script for Construction Industry Agents

set -e  # Exit on any error

# Configuration
ENVIRONMENT=${1:-production}
CONFIG_FILE="config.${ENVIRONMENT}.json"
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"

echo "Starting deployment for environment: $ENVIRONMENT"

# 1. Pre-deployment checks
echo "Running pre-deployment checks..."
./scripts/pre_deployment_checks.sh

# 2. Backup current system
echo "Creating backup..."
mkdir -p "$BACKUP_DIR"
./scripts/backup_system.sh "$BACKUP_DIR"

# 3. Environment setup
echo "Setting up environment..."
./scripts/setup_environment.sh "$ENVIRONMENT"

# 4. Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# 5. Configure system
echo "Configuring system..."
./scripts/configure_system.sh "$CONFIG_FILE"

# 6. Initialize database
echo "Initializing database..."
python scripts/init_database.py

# 7. Run tests
echo "Running post-deployment tests..."
python test_suite.py

# 8. Start services
echo "Starting services..."
./scripts/start_services.sh

echo "Deployment completed successfully!"
```

Provide complete deployment scripts with error handling and rollback procedures.
```

## Documentation Prompts

### API Documentation

#### Prompt 13: Create API Documentation
```
Create comprehensive API documentation for the Construction Industry Agents system:

**Documentation Requirements**:
1. **Agent APIs**: Document all agent interfaces and methods
2. **Data Models**: Document all data structures and formats
3. **Workflow APIs**: Document workflow orchestration interfaces
4. **Error Handling**: Document error codes and handling procedures
5. **Examples**: Provide usage examples for all major functions
6. **Integration Guide**: Guide for integrating with external systems

**Documentation Structure**:
```markdown
# Construction Industry Agents API Documentation

## Overview
Brief description of the system and its capabilities

## Quick Start
Basic setup and usage examples

## Agents

### Excel Parser Agent
**Purpose**: Parse Excel construction specifications
**Input**: Excel file path
**Output**: List of ConstructionItem objects

#### Methods
- `parse_excel(file_path: str) -> List[ConstructionItem]`
- `validate_file(file_path: str) -> bool`
- `get_parsing_stats() -> Dict[str, Any]`

#### Example Usage
```python
from excel_parser_agent import ExcelParserAgent

agent = ExcelParserAgent()
items = agent.parse_excel("construction_spec.xlsx")
print(f"Parsed {len(items)} items")
```

## Data Models

### ConstructionItem
```python
@dataclass
class ConstructionItem:
    position_number: str
    description: str
    unit: str
    quantity: float
    # ... other fields
```

## Error Handling

### Error Codes
- `E001`: File not found
- `E002`: Invalid file format
- `E003`: API authentication failed
- `E004`: Processing timeout

### Error Handling Examples
```python
try:
    result = agent.process(data)
except AgentError as e:
    if e.code == "E001":
        # Handle file not found
        pass
```

## Integration Guide

### External System Integration
Step-by-step guide for integrating with external systems

### Webhook Integration
Guide for webhook-based integration
```

Provide complete API documentation with examples and integration guides.
```

### User Documentation

#### Prompt 14: Create User Guide
```
Create a comprehensive user guide for the Construction Industry Agents system:

**Guide Requirements**:
1. **Getting Started**: Installation, setup, and first use
2. **Basic Operations**: Common tasks and workflows
3. **Advanced Features**: Advanced configuration and customization
4. **Troubleshooting**: Common issues and solutions
5. **Best Practices**: Recommended usage patterns
6. **FAQ**: Frequently asked questions and answers

**Guide Structure**:
```markdown
# Construction Industry Agents User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Operations](#basic-operations)
3. [Advanced Features](#advanced-features)
4. [Troubleshooting](#troubleshooting)
5. [Best Practices](#best-practices)
6. [FAQ](#faq)

## Getting Started

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Construction specification Excel files

### Installation
```bash
# Clone the repository
git clone https://github.com/Prosperity-labs/construction-industry-agents.git
cd construction-industry-agents

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="your-api-key"
```

### First Use
```bash
# Process your first construction specification
python workflow_orchestrator.py your_specification.xlsx
```

## Basic Operations

### Processing Construction Specifications
Step-by-step guide for processing construction specifications

### Understanding Output
Explanation of generated quotes and documents

### Customizing Processing
Guide for customizing processing parameters

## Advanced Features

### Custom Supplier Mapping
Guide for customizing supplier mappings

### Performance Optimization
Tips for optimizing processing performance

### Integration with External Systems
Guide for integrating with external systems

## Troubleshooting

### Common Issues
- API authentication errors
- File format issues
- Processing errors
- Performance problems

### Solutions
Detailed solutions for each common issue

## Best Practices

### File Preparation
Best practices for preparing Excel files

### System Configuration
Recommended configuration settings

### Performance Optimization
Tips for optimal performance

## FAQ

### General Questions
Q: How accurate is the categorization?
A: The system achieves 99%+ accuracy using OpenAI GPT-4...

### Technical Questions
Q: What file formats are supported?
A: The system supports Excel files (.xlsx) exported from Revit...

### Business Questions
Q: How much does it cost to process a project?
A: Processing costs range from €0.02 to €0.25 per project...
```

Provide complete user guide with practical examples and troubleshooting information.
```

## Conclusion

These derived prompts provide comprehensive guidance for working with the Construction Industry Agents system. They cover development, testing, operations, configuration, deployment, and documentation aspects of the system.

Each prompt is designed to be specific, actionable, and aligned with the system's architecture and best practices. They can be used by developers, operators, and users to effectively work with and maintain the system.

For additional prompts or customization, refer to the system documentation or contact the development team. 