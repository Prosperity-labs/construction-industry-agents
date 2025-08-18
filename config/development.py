"""Development configuration"""

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
