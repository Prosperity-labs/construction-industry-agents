# Runbook - Construction Industry Agents

## System Overview

The Construction Industry Agents system is an AI-powered automation platform that processes construction specifications and generates professional quotes. This runbook provides operational procedures, troubleshooting guides, and maintenance instructions.

## Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Required Python packages (see `requirements.txt`)

### Initial Setup
```bash
# Clone repository
git clone https://github.com/Prosperity-labs/construction-industry-agents.git
cd construction-industry-agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY="your-openai-api-key"
```

### Basic Operation
```bash
# Run complete workflow
python workflow_orchestrator.py test_construction_spec.xlsx

# Run individual agent
python excel_parser_agent.py test_construction_spec.xlsx

# Run system demo
python demo_system.py

# Run test suite
python test_suite.py
```

## Operational Procedures

### Daily Operations

#### 1. System Health Check
```bash
# Check system status
python test_suite.py

# Verify all agents are operational
python -c "
from workflow_orchestrator import WorkflowOrchestrator
orchestrator = WorkflowOrchestrator()
print('✅ System operational')
"
```

#### 2. Process Construction Specifications
```bash
# Process single file
python workflow_orchestrator.py /path/to/construction_spec.xlsx

# Process multiple files
for file in /path/to/specs/*.xlsx; do
    python workflow_orchestrator.py "$file"
done

# Process with custom output directory
python workflow_orchestrator.py input.xlsx --output-dir /custom/output/path
```

#### 3. Monitor Processing
```bash
# Check processing logs
tail -f logs/workflow.log

# Monitor output directory
watch -n 5 "ls -la complete_workflow_output/"

# Check OpenAI API usage
python -c "
import openai
client = openai.OpenAI()
# Check usage (requires appropriate permissions)
"
```

### Weekly Operations

#### 1. Performance Review
```bash
# Generate performance report
python test_runner.py --performance-report

# Analyze processing times
python -c "
import json
with open('performance_metrics.json', 'r') as f:
    metrics = json.load(f)
print(f'Average processing time: {metrics[\"avg_time\"]}s')
print(f'Success rate: {metrics[\"success_rate\"]}%')
"
```

#### 2. Data Backup
```bash
# Backup output files
tar -czf backup_$(date +%Y%m%d).tar.gz complete_workflow_output/

# Backup configuration
cp requirements.txt backup/
cp .env backup/  # if using .env file
```

#### 3. System Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update OpenAI API client
pip install --upgrade openai

# Test system after updates
python test_suite.py
```

### Monthly Operations

#### 1. Supplier Database Maintenance
```python
# Review and update supplier mappings
python -c "
from supplier_mapping_agent import SupplierMappingAgent
agent = SupplierMappingAgent()
# Review supplier database
suppliers = agent._load_suppliers_database()
print(f'Total suppliers: {len(suppliers)}')
"
```

#### 2. Performance Optimization
```bash
# Analyze processing bottlenecks
python test_runner.py --performance-analysis

# Optimize batch sizes
python -c "
# Adjust batch processing parameters based on performance data
"
```

#### 3. Security Review
```bash
# Check for security vulnerabilities
pip audit

# Review API key usage
python -c "
import os
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print('✅ API key configured')
    print(f'Key length: {len(api_key)}')
else:
    print('❌ API key not found')
"
```

## Troubleshooting Guide

### Common Issues

#### 1. OpenAI API Errors

**Symptoms:**
- `openai.AuthenticationError`
- `openai.RateLimitError`
- `openai.APIError`

**Diagnosis:**
```bash
# Check API key
echo $OPENAI_API_KEY | wc -c

# Test API connection
python -c "
import openai
client = openai.OpenAI()
try:
    response = client.chat.completions.create(
        model='gpt-4',
        messages=[{'role': 'user', 'content': 'test'}],
        max_tokens=5
    )
    print('✅ API connection successful')
except Exception as e:
    print(f'❌ API error: {e}')
"
```

**Solutions:**
- Verify API key is correct and has sufficient credits
- Check rate limits and implement backoff
- Ensure network connectivity to OpenAI servers

#### 2. Excel File Processing Errors

**Symptoms:**
- `FileNotFoundError`
- `openpyxl.utils.exceptions.InvalidFileException`
- Parsing errors in output

**Diagnosis:**
```bash
# Check file existence and format
python -c "
import pandas as pd
try:
    df = pd.read_excel('problematic_file.xlsx')
    print(f'✅ File readable, {len(df)} rows')
except Exception as e:
    print(f'❌ File error: {e}')
"
```

**Solutions:**
- Verify file path and permissions
- Check Excel file format compatibility
- Validate file structure matches expected format

#### 3. Memory Issues

**Symptoms:**
- `MemoryError`
- Slow processing with large files
- System becomes unresponsive

**Diagnosis:**
```bash
# Check memory usage
python -c "
import psutil
memory = psutil.virtual_memory()
print(f'Memory usage: {memory.percent}%')
print(f'Available: {memory.available / 1024**3:.1f} GB')
"
```

**Solutions:**
- Reduce batch size in processing
- Implement streaming for large files
- Add memory monitoring and limits

#### 4. Network Connectivity Issues

**Symptoms:**
- Timeout errors
- Connection refused
- Slow response times

**Diagnosis:**
```bash
# Test network connectivity
ping api.openai.com
curl -I https://api.openai.com

# Check DNS resolution
nslookup api.openai.com
```

**Solutions:**
- Check internet connectivity
- Verify firewall settings
- Implement retry logic with exponential backoff

### Error Recovery Procedures

#### 1. Partial Processing Recovery
```python
# Resume processing from last successful step
def resume_processing(workflow_id: str, last_step: str):
    """Resume workflow from specific step"""
    orchestrator = WorkflowOrchestrator()
    
    # Load previous state
    state_file = f"workflow_state_{workflow_id}.json"
    with open(state_file, 'r') as f:
        state = json.load(f)
    
    # Resume from last successful step
    if last_step == "excel_parsing":
        # Resume from supplier mapping
        pass
    elif last_step == "supplier_mapping":
        # Resume from communication
        pass
    # ... continue for other steps
```

#### 2. Data Corruption Recovery
```python
# Recover from corrupted data
def recover_corrupted_data(file_path: str):
    """Attempt to recover corrupted Excel file"""
    try:
        # Try different Excel readers
        import pandas as pd
        df = pd.read_excel(file_path, engine='openpyxl')
    except:
        try:
            df = pd.read_excel(file_path, engine='xlrd')
        except:
            # Try CSV conversion
            df = pd.read_csv(file_path.replace('.xlsx', '.csv'))
    
    return df
```

#### 3. API Rate Limit Recovery
```python
# Handle rate limiting
def handle_rate_limit(func, max_retries=5, base_delay=1):
    """Retry function with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return func()
        except openai.RateLimitError:
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
            continue
        except Exception as e:
            raise e
    
    raise Exception("Max retries exceeded")
```

## Maintenance Procedures

### Regular Maintenance

#### 1. Log Rotation
```bash
# Rotate log files
logrotate -f /etc/logrotate.d/construction-agents

# Manual log rotation
mv logs/workflow.log logs/workflow.log.$(date +%Y%m%d)
gzip logs/workflow.log.$(date +%Y%m%d)
```

#### 2. Temporary File Cleanup
```bash
# Clean temporary files
find /tmp -name "construction_agents_*" -mtime +7 -delete

# Clean output directories
find complete_workflow_output/ -name "*.tmp" -delete
```

#### 3. Database Maintenance
```python
# Clean up old workflow data
def cleanup_old_workflows(days_old=30):
    """Remove workflow data older than specified days"""
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    # Clean workflow output files
    output_dir = Path("complete_workflow_output")
    for file in output_dir.glob("*"):
        if file.stat().st_mtime < cutoff_date.timestamp():
            file.unlink()
```

### Performance Tuning

#### 1. Batch Size Optimization
```python
# Optimize batch sizes based on performance
def optimize_batch_sizes():
    """Determine optimal batch sizes for processing"""
    test_sizes = [5, 10, 20, 50]
    results = {}
    
    for size in test_sizes:
        start_time = time.time()
        # Test processing with batch size
        processing_time = time.time() - start_time
        results[size] = processing_time
    
    optimal_size = min(results, key=results.get)
    return optimal_size
```

#### 2. Memory Optimization
```python
# Monitor and optimize memory usage
def optimize_memory_usage():
    """Monitor and optimize memory consumption"""
    import psutil
    import gc
    
    # Force garbage collection
    gc.collect()
    
    # Monitor memory usage
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        # Implement memory optimization strategies
        pass
```

#### 3. API Usage Optimization
```python
# Optimize OpenAI API usage
def optimize_api_usage():
    """Optimize API calls for cost and performance"""
    # Implement caching for similar requests
    # Batch similar requests together
    # Use appropriate model for task complexity
    pass
```

## Monitoring and Alerting

### Key Metrics to Monitor

#### 1. Processing Performance
- Average processing time per item
- Success rate percentage
- Error rate and types
- API response times

#### 2. Resource Usage
- CPU utilization
- Memory consumption
- Disk space usage
- Network bandwidth

#### 3. Business Metrics
- Number of quotes generated
- Cost per quote
- Customer satisfaction scores
- Supplier response rates

### Alerting Setup

#### 1. Error Alerts
```python
# Set up error alerting
def send_error_alert(error: Exception, context: dict):
    """Send error alert to operations team"""
    alert_message = {
        "severity": "high",
        "error": str(error),
        "context": context,
        "timestamp": datetime.now().isoformat()
    }
    
    # Send via email, Slack, or other notification system
    # Implementation depends on available notification systems
```

#### 2. Performance Alerts
```python
# Monitor performance thresholds
def check_performance_thresholds():
    """Check if performance metrics exceed thresholds"""
    thresholds = {
        "processing_time": 300,  # 5 minutes
        "error_rate": 0.05,      # 5%
        "memory_usage": 0.8      # 80%
    }
    
    # Check current metrics against thresholds
    # Send alerts if thresholds exceeded
```

#### 3. Health Check Alerts
```python
# Automated health checks
def health_check():
    """Perform system health check"""
    checks = [
        check_api_connectivity,
        check_file_system,
        check_memory_usage,
        check_processing_queue
    ]
    
    results = {}
    for check in checks:
        try:
            results[check.__name__] = check()
        except Exception as e:
            results[check.__name__] = f"FAILED: {e}"
    
    return results
```

## Backup and Recovery

### Backup Procedures

#### 1. Configuration Backup
```bash
# Backup configuration files
tar -czf config_backup_$(date +%Y%m%d).tar.gz \
    requirements.txt \
    *.py \
    diagrams/ \
    tests/
```

#### 2. Data Backup
```bash
# Backup output data
rsync -av complete_workflow_output/ /backup/workflow_output/

# Backup test data
rsync -av tests/ /backup/test_data/
```

#### 3. Database Backup
```python
# Backup supplier database
def backup_supplier_database():
    """Backup supplier mapping data"""
    from supplier_mapping_agent import SupplierMappingAgent
    
    agent = SupplierMappingAgent()
    suppliers = agent._load_suppliers_database()
    
    backup_file = f"supplier_backup_{datetime.now().strftime('%Y%m%d')}.json"
    with open(backup_file, 'w') as f:
        json.dump([s.__dict__ for s in suppliers], f, indent=2)
```

### Recovery Procedures

#### 1. System Recovery
```bash
# Restore from backup
tar -xzf config_backup_20231201.tar.gz

# Restore data
rsync -av /backup/workflow_output/ complete_workflow_output/

# Verify restoration
python test_suite.py
```

#### 2. Configuration Recovery
```python
# Restore configuration
def restore_configuration(backup_date: str):
    """Restore system configuration from backup"""
    backup_file = f"config_backup_{backup_date}.tar.gz"
    
    # Extract backup
    import tarfile
    with tarfile.open(backup_file, 'r:gz') as tar:
        tar.extractall()
    
    # Verify restoration
    python test_suite.py
```

## Security Procedures

### Access Control

#### 1. API Key Management
```bash
# Rotate API keys regularly
export OPENAI_API_KEY="new-api-key"

# Verify key permissions
python -c "
import openai
client = openai.OpenAI()
# Test API access with minimal request
"
```

#### 2. File Permissions
```bash
# Set appropriate file permissions
chmod 600 .env  # if using .env file
chmod 755 *.py
chmod 644 *.md
```

#### 3. Audit Logging
```python
# Implement audit logging
def audit_log(action: str, user: str, details: dict):
    """Log security-relevant actions"""
    audit_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "user": user,
        "details": details,
        "ip_address": get_client_ip()
    }
    
    with open("audit.log", "a") as f:
        json.dump(audit_entry, f)
        f.write("\n")
```

### Incident Response

#### 1. Security Incident Response
```python
# Security incident response procedure
def handle_security_incident(incident_type: str, details: dict):
    """Handle security incidents"""
    # 1. Assess severity
    severity = assess_severity(incident_type, details)
    
    # 2. Contain incident
    if severity == "high":
        isolate_system()
    
    # 3. Investigate
    investigation_results = investigate_incident(details)
    
    # 4. Remediate
    remediate_incident(investigation_results)
    
    # 5. Report
    report_incident(incident_type, details, investigation_results)
```

## Emergency Procedures

### System Outage Response

#### 1. Immediate Actions
```bash
# Stop all processing
pkill -f "python.*workflow_orchestrator"

# Check system status
python test_suite.py

# Notify stakeholders
# Send outage notification
```

#### 2. Recovery Steps
```bash
# Restart system components
python workflow_orchestrator.py --health-check

# Verify functionality
python test_suite.py

# Resume processing
python workflow_orchestrator.py pending_files.xlsx
```

### Data Loss Recovery

#### 1. Assess Data Loss
```python
# Assess extent of data loss
def assess_data_loss():
    """Determine what data has been lost"""
    # Check file system integrity
    # Identify missing files
    # Determine recovery options
    pass
```

#### 2. Recovery Options
```python
# Implement data recovery
def recover_lost_data():
    """Attempt to recover lost data"""
    # Check backup availability
    # Restore from backups
    # Re-process if necessary
    pass
```

## Conclusion

This runbook provides comprehensive operational procedures for the Construction Industry Agents system. Regular review and updates of these procedures ensure reliable system operation and quick resolution of issues.

For additional support or questions, refer to the system documentation or contact the development team. 