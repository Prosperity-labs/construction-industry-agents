#!/usr/bin/env python3
"""
Project Restructuring Tool
Reorganizes the scattered codebase into proper domain-driven architecture
"""

import os
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProjectRestructurer:
    """Restructures the project into proper domain architecture"""
    
    def __init__(self):
        self.root_path = Path(".")
        self.new_structure = {
            "src": {
                "core": {
                    "__init__.py": "",
                    "models": {
                        "__init__.py": "",
                        "construction_item.py": "",
                        "supplier.py": "",
                        "quote.py": "",
                        "workflow.py": ""
                    },
                    "exceptions": {
                        "__init__.py": "",
                        "base.py": "",
                        "parsing.py": "",
                        "workflow.py": ""
                    },
                    "interfaces": {
                        "__init__.py": "",
                        "agent_interface.py": "",
                        "parser_interface.py": "",
                        "communicator_interface.py": "",
                        "generator_interface.py": ""
                    }
                },
                "domains": {
                    "__init__.py": "",
                    "parsing": {
                        "__init__.py": "",
                        "services": {
                            "__init__.py": "",
                            "excel_parser_service.py": "",
                            "document_analyzer_service.py": ""
                        },
                        "agents": {
                            "__init__.py": "",
                            "excel_parser_agent.py": ""
                        }
                    },
                    "suppliers": {
                        "__init__.py": "",
                        "services": {
                            "__init__.py": "",
                            "supplier_mapping_service.py": "",
                            "supplier_database_service.py": ""
                        },
                        "agents": {
                            "__init__.py": "",
                            "supplier_mapping_agent.py": ""
                        },
                        "repositories": {
                            "__init__.py": "",
                            "supplier_repository.py": ""
                        }
                    },
                    "communication": {
                        "__init__.py": "",
                        "services": {
                            "__init__.py": "",
                            "email_service.py": "",
                            "api_service.py": "",
                            "communication_service.py": ""
                        },
                        "agents": {
                            "__init__.py": "",
                            "communication_agent.py": ""
                        }
                    },
                    "responses": {
                        "__init__.py": "",
                        "services": {
                            "__init__.py": "",
                            "response_parser_service.py": "",
                            "ocr_service.py": "",
                            "price_extraction_service.py": ""
                        },
                        "agents": {
                            "__init__.py": "",
                            "response_parser_agent.py": ""
                        }
                    },
                    "quotes": {
                        "__init__.py": "",
                        "services": {
                            "__init__.py": "",
                            "quote_calculation_service.py": "",
                            "pricing_optimization_service.py": ""
                        },
                        "agents": {
                            "__init__.py": "",
                            "quote_calculator_agent.py": ""
                        }
                    },
                    "documents": {
                        "__init__.py": "",
                        "services": {
                            "__init__.py": "",
                            "document_generation_service.py": "",
                            "template_service.py": "",
                            "export_service.py": ""
                        },
                        "agents": {
                            "__init__.py": "",
                            "document_generator_agent.py": ""
                        }
                    }
                },
                "workflow": {
                    "__init__.py": "",
                    "orchestrators": {
                        "__init__.py": "",
                        "workflow_orchestrator.py": "",
                        "visual_workflow_orchestrator.py": "",
                        "web_workflow_orchestrator.py": ""
                    },
                    "builders": {
                        "__init__.py": "",
                        "system_builder.py": "",
                        "diagram_parser.py": ""
                    }
                },
                "infrastructure": {
                    "__init__.py": "",
                    "config": {
                        "__init__.py": "",
                        "settings.py": "",
                        "logging_config.py": ""
                    },
                    "persistence": {
                        "__init__.py": "",
                        "file_storage.py": "",
                        "session_storage.py": ""
                    },
                    "external": {
                        "__init__.py": "",
                        "openai_client.py": "",
                        "email_client.py": ""
                    }
                },
                "web": {
                    "__init__.py": "",
                    "api": {
                        "__init__.py": "",
                        "routes": {
                            "__init__.py": "",
                            "demo_routes.py": "",
                            "workflow_routes.py": "",
                            "health_routes.py": ""
                        },
                        "middleware": {
                            "__init__.py": "",
                            "cors_middleware.py": "",
                            "error_middleware.py": ""
                        }
                    },
                    "frontend": {
                        "__init__.py": "",
                        "app.py": "",
                        "templates": {},
                        "static": {
                            "css": {},
                            "js": {},
                            "images": {}
                        }
                    }
                },
                "testing": {
                    "__init__.py": "",
                    "framework": {
                        "__init__.py": "",
                        "test_runner.py": "",
                        "visual_test_runner.py": "",
                        "performance_tester.py": ""
                    },
                    "fixtures": {
                        "__init__.py": "",
                        "excel_fixtures.py": "",
                        "supplier_fixtures.py": ""
                    }
                }
            },
            "tests": {
                "__init__.py": "",
                "unit": {
                    "__init__.py": "",
                    "domains": {
                        "__init__.py": "",
                        "test_parsing.py": "",
                        "test_suppliers.py": "",
                        "test_communication.py": "",
                        "test_responses.py": "",
                        "test_quotes.py": "",
                        "test_documents.py": ""
                    },
                    "workflow": {
                        "__init__.py": "",
                        "test_orchestrator.py": "",
                        "test_builder.py": ""
                    }
                },
                "integration": {
                    "__init__.py": "",
                    "test_full_workflow.py": "",
                    "test_web_api.py": ""
                },
                "e2e": {
                    "__init__.py": "",
                    "test_complete_system.py": ""
                },
                "fixtures": {
                    "excel_files": {},
                    "mock_responses": {},
                    "expected_outputs": {}
                }
            },
            "docs": {
                "api": {},
                "architecture": {},
                "user_guides": {},
                "deployment": {}
            },
            "scripts": {
                "setup.py": "",
                "deploy.py": "",
                "migration.py": ""
            },
            "config": {
                "development.py": "",
                "production.py": "",
                "testing.py": ""
            }
        }
    
    def create_directory_structure(self):
        """Create the new directory structure"""
        logger.info("🏗️ Creating new directory structure...")
        
        def create_nested_dirs(base_path: Path, structure: dict):
            for name, content in structure.items():
                path = base_path / name
                
                if isinstance(content, dict):
                    path.mkdir(parents=True, exist_ok=True)
                    create_nested_dirs(path, content)
                else:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    if not path.exists():
                        path.touch()
        
        create_nested_dirs(self.root_path, self.new_structure)
        logger.info("✅ Directory structure created")
    
    def move_existing_files(self):
        """Move existing files to their proper locations"""
        logger.info("📦 Moving existing files to proper locations...")
        
        file_mappings = {
            # Core models
            "excel_parser_agent.py": "src/domains/parsing/agents/excel_parser_agent.py",
            "supplier_mapping_agent.py": "src/domains/suppliers/agents/supplier_mapping_agent.py", 
            "communication_agent.py": "src/domains/communication/agents/communication_agent.py",
            "response_parser_agent.py": "src/domains/responses/agents/response_parser_agent.py",
            "quote_calculator_agent.py": "src/domains/quotes/agents/quote_calculator_agent.py",
            "document_generator_agent.py": "src/domains/documents/agents/document_generator_agent.py",
            
            # Workflow
            "workflow_orchestrator.py": "src/workflow/orchestrators/workflow_orchestrator.py",
            "visual_workflow_monitor.py": "src/workflow/orchestrators/visual_workflow_orchestrator.py",
            "system_builder.py": "src/workflow/builders/system_builder.py",
            
            # Web
            "web_frontend.py": "src/web/frontend/app.py",
            
            # Testing
            "test_runner.py": "src/testing/framework/test_runner.py",
            "test_suite.py": "src/testing/framework/visual_test_runner.py",
            
            # Scripts
            "launch_demo.py": "scripts/launch_demo.py",
            "demo_system.py": "scripts/demo_system.py",
            "simple_visual_demo.py": "scripts/simple_visual_demo.py",
            
            # Docs
            "DEMO_README.md": "docs/user_guides/DEMO_README.md",
            "README.md": "docs/README.md"
        }
        
        for source, target in file_mappings.items():
            source_path = Path(source)
            target_path = Path(target)
            
            if source_path.exists():
                target_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(str(source_path), str(target_path))
                    logger.info(f"  ✅ Moved {source} → {target}")
                except Exception as e:
                    logger.warning(f"  ⚠️ Could not move {source}: {str(e)}")
    
    def create_init_files(self):
        """Create proper __init__.py files with imports"""
        logger.info("📝 Creating __init__.py files...")
        
        init_contents = {
            "src/__init__.py": '"""Construction Industry Agents - Source Code"""',
            
            "src/core/__init__.py": '''"""Core domain models and interfaces"""
from .models import *
from .interfaces import *
from .exceptions import *
''',
            
            "src/core/models/__init__.py": '''"""Core domain models"""
from .construction_item import ConstructionItem
from .supplier import Supplier, SupplierMatch
from .quote import Quote, QuoteItem, QuoteCalculation
from .workflow import WorkflowSession, WorkflowStep
''',
            
            "src/domains/__init__.py": '''"""Domain modules"""
from . import parsing
from . import suppliers
from . import communication
from . import responses
from . import quotes
from . import documents
''',
            
            "src/domains/parsing/__init__.py": '''"""Parsing domain"""
from .agents.excel_parser_agent import ExcelParserAgent
from .services.excel_parser_service import ExcelParserService
''',
            
            "src/workflow/__init__.py": '''"""Workflow orchestration"""
from .orchestrators.workflow_orchestrator import WorkflowOrchestrator
from .orchestrators.visual_workflow_orchestrator import VisualWorkflowOrchestrator
from .builders.system_builder import SystemBuilder
''',
            
            "src/infrastructure/__init__.py": '''"""Infrastructure layer"""
from .config.settings import Settings
from .external.openai_client import OpenAIClient
''',
            
            "src/web/__init__.py": '''"""Web interface"""
from .frontend.app import create_app
''',
            
            "tests/__init__.py": '''"""Test suite"""
''',
        }
        
        for file_path, content in init_contents.items():
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        logger.info("✅ __init__.py files created")
    
    def create_main_entry_points(self):
        """Create main entry points"""
        logger.info("🚀 Creating main entry points...")
        
        # Main application entry point
        main_app_content = '''#!/usr/bin/env python3
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
'''
        
        with open("main.py", 'w', encoding='utf-8') as f:
            f.write(main_app_content)
        
        # Setup script
        setup_content = '''#!/usr/bin/env python3
"""
Setup script for Construction Industry Agents
"""

import subprocess
import sys
from pathlib import Path

def setup_environment():
    """Set up the development environment"""
    print("🏗️ Setting up Construction Industry Agents...")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"])
    
    # Install requirements
    print("📋 Installing requirements...")
    pip_cmd = "venv/bin/pip" if sys.platform != "win32" else "venv\\\\Scripts\\\\pip"
    subprocess.run([pip_cmd, "install", "-r", "requirements.txt"])
    
    # Run system builder
    print("🔨 Building system components...")
    python_cmd = "venv/bin/python" if sys.platform != "win32" else "venv\\\\Scripts\\\\python"
    subprocess.run([python_cmd, "src/workflow/builders/system_builder.py"])
    
    print("✅ Setup completed!")
    print("🚀 Run: python main.py demo")

if __name__ == "__main__":
    setup_environment()
'''
        
        with open("scripts/setup.py", 'w', encoding='utf-8') as f:
            f.write(setup_content)
        
        logger.info("✅ Entry points created")
    
    def create_configuration_files(self):
        """Create configuration files"""
        logger.info("⚙️ Creating configuration files...")
        
        # Development config
        dev_config = '''"""Development configuration"""

import os

class DevelopmentConfig:
    """Development environment configuration"""
    
    DEBUG = True
    TESTING = False
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    
    # Web Configuration
    WEB_HOST = "0.0.0.0"
    WEB_PORT = 5000
    
    # File Paths
    TEMPLATES_DIR = "src/web/frontend/templates"
    STATIC_DIR = "src/web/frontend/static"
    OUTPUT_DIR = "output"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Demo Configuration
    DEMO_EXCEL_FILE = "tests/fixtures/excel_files/demo_construction_spec.xlsx"
    DEMO_PROCESSING_DELAY = 1.0  # seconds between steps for visual effect
'''
        
        with open("config/development.py", 'w', encoding='utf-8') as f:
            f.write(dev_config)
        
        # Project configuration
        project_config = '''"""Project configuration and constants"""

from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"
DOCS_DIR = PROJECT_ROOT / "docs"

# Domain mappings
CONSTRUCTION_CATEGORIES = {
    'mehanika': 'HVAC dobavljač',
    'elektro': 'Elektro dobavljač', 
    'izolacija': 'Izolacioni materijali',
    'montaža': 'Izvođačke usluge',
    'građevina': 'Građevinski materijali',
    'vodovodne_instalacije': 'Sanitarne instalacije',
    'infrastruktura': 'Infrastrukturni radovi',
    'demontaža': 'Demolicija i uklanjanje',
    'transport': 'Transport i logistika',
    'ostalo': 'Opšti dobavljač'
}

# Business rules
DEFAULT_MARGIN = 0.15  # 15%
TAX_RATE = 0.20  # 20% VAT
CURRENCY = "RSD"

# System information
SYSTEM_NAME = "Construction Industry Agents"
SYSTEM_VERSION = "1.0.0"
SYSTEM_DESCRIPTION = "AI-powered construction specification processing"
'''
        
        with open("src/infrastructure/config/settings.py", 'w', encoding='utf-8') as f:
            f.write(project_config)
        
        logger.info("✅ Configuration files created")
    
    def update_imports_in_moved_files(self):
        """Update import statements in moved files"""
        logger.info("🔄 Updating import statements...")
        
        # This would be a complex operation to update all imports
        # For now, we'll create a simple import fix script
        import_fix_content = '''#!/usr/bin/env python3
"""
Import Fix Script
Updates import statements after restructuring
"""

import os
import re
from pathlib import Path

def fix_imports():
    """Fix import statements in all Python files"""
    
    import_mappings = {
        "from excel_parser_agent import": "from src.domains.parsing.agents.excel_parser_agent import",
        "from supplier_mapping_agent import": "from src.domains.suppliers.agents.supplier_mapping_agent import",
        "from communication_agent import": "from src.domains.communication.agents.communication_agent import",
        "from response_parser_agent import": "from src.domains.responses.agents.response_parser_agent import",
        "from quote_calculator_agent import": "from src.domains.quotes.agents.quote_calculator_agent import",
        "from document_generator_agent import": "from src.domains.documents.agents.document_generator_agent import",
    }
    
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                file_path = Path(root) / file
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    updated = False
                    for old_import, new_import in import_mappings.items():
                        if old_import in content:
                            content = content.replace(old_import, new_import)
                            updated = True
                    
                    if updated:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Updated imports in: {file_path}")
                        
                except Exception as e:
                    print(f"Error updating {file_path}: {e}")

if __name__ == "__main__":
    fix_imports()
'''
        
        with open("scripts/fix_imports.py", 'w', encoding='utf-8') as f:
            f.write(import_fix_content)
        
        logger.info("✅ Import fix script created")
    
    def create_documentation(self):
        """Create updated documentation"""
        logger.info("📚 Creating documentation...")
        
        architecture_doc = '''# 🏗️ Construction Industry Agents - Architecture

## 📊 Domain-Driven Design Structure

```
src/
├── core/                    # Core domain models and interfaces
│   ├── models/             # Domain entities
│   ├── interfaces/         # Abstract interfaces
│   └── exceptions/         # Domain exceptions
│
├── domains/                # Business domains
│   ├── parsing/            # Excel parsing domain
│   ├── suppliers/          # Supplier management domain  
│   ├── communication/      # Communication domain
│   ├── responses/          # Response processing domain
│   ├── quotes/             # Quote calculation domain
│   └── documents/          # Document generation domain
│
├── workflow/               # Workflow orchestration
│   ├── orchestrators/      # Workflow coordinators
│   └── builders/           # System builders
│
├── infrastructure/         # Infrastructure concerns
│   ├── config/            # Configuration
│   ├── persistence/       # Data storage
│   └── external/          # External services
│
├── web/                   # Web interface
│   ├── api/               # REST API
│   └── frontend/          # Web frontend
│
└── testing/               # Testing framework
    ├── framework/         # Test runners
    └── fixtures/          # Test data
```

## 🎯 Domain Responsibilities

### **Parsing Domain**
- Excel file analysis
- Construction item extraction
- Data validation

### **Suppliers Domain** 
- Supplier database management
- Category-based matching
- Performance tracking

### **Communication Domain**
- Multi-channel messaging
- Request templating
- Response tracking

### **Responses Domain**
- Email/PDF parsing
- Price extraction
- Data validation

### **Quotes Domain**
- Price optimization
- Margin calculation
- Business rules

### **Documents Domain**
- Template management
- PDF/Excel generation
- Professional formatting

## 🔄 Data Flow

1. **Parsing** → Extracts construction items
2. **Suppliers** → Maps items to suppliers  
3. **Communication** → Sends requests
4. **Responses** → Processes replies
5. **Quotes** → Calculates optimal pricing
6. **Documents** → Generates deliverables

## 🧪 Testing Strategy

- **Unit Tests**: Each domain isolated
- **Integration Tests**: Cross-domain workflows
- **E2E Tests**: Complete system validation
- **Performance Tests**: Speed and accuracy metrics
'''
        
        with open("docs/architecture/domain_design.md", 'w', encoding='utf-8') as f:
            f.write(architecture_doc)
        
        logger.info("✅ Documentation created")
    
    def restructure_project(self):
        """Execute the complete restructuring"""
        logger.info("🏗️ Starting project restructuring...")
        
        # Create backup
        backup_dir = Path("backup_old_structure")
        if not backup_dir.exists():
            logger.info("💾 Creating backup of current structure...")
            shutil.copytree(".", backup_dir, ignore=shutil.ignore_patterns(
                'venv', '__pycache__', '*.pyc', '.git', 'backup_*'
            ))
        
        # Execute restructuring steps
        self.create_directory_structure()
        self.move_existing_files()
        self.create_init_files()
        self.create_main_entry_points()
        self.create_configuration_files()
        self.update_imports_in_moved_files()
        self.create_documentation()
        
        logger.info("✅ Project restructuring completed!")
        logger.info("🚀 New structure ready for development")
        
        print(f"""
🎉 PROJECT RESTRUCTURING COMPLETED!

📁 New Structure:
  • src/domains/          - Business domains with clean separation
  • src/workflow/         - Orchestration layer
  • src/infrastructure/   - Cross-cutting concerns
  • src/web/             - Web interface
  • tests/               - Comprehensive test suite
  • docs/                - Documentation
  • scripts/             - Utility scripts
  • config/              - Environment configurations

🚀 Next Steps:
  1. Run: python scripts/setup.py
  2. Run: python scripts/fix_imports.py
  3. Run: python main.py demo

📚 Documentation: docs/architecture/domain_design.md
        """)

def main():
    """Main restructuring function"""
    restructurer = ProjectRestructurer()
    restructurer.restructure_project()

if __name__ == "__main__":
    main()