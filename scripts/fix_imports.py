#!/usr/bin/env python3
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
