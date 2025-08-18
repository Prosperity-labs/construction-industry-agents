"""Project configuration and constants"""

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
