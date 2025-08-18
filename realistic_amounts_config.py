#!/usr/bin/env python3
"""
Realistic Amounts Configuration
Adjusts financial parameters to realistic construction industry values
"""

import os
from pathlib import Path

class RealisticAmountsConfig:
    """Configuration for realistic construction industry amounts"""
    
    # Currency and formatting
    CURRENCY = "EUR"  # More internationally recognizable
    CURRENCY_SYMBOL = "€"
    
    # Realistic price multipliers (increase current amounts)
    PRICE_MULTIPLIER = 25.0  # Multiply current RSD amounts by 25
    
    # Realistic unit prices based on actual Serbian construction specification (realistic_test_v1.xlsx)
    REALISTIC_UNIT_PRICES = {
        'mehanika': {
            'min': 150,   # €150 for HVAC work
            'max': 800,   # €800 for complex systems
            'default': 350
        },
        'elektro': {
            'min': 80,    # €80 for electrical work
            'max': 500,   # €500 for complex installations
            'default': 200
        },
        'izolacija': {
            'min': 25,    # €25 per m² for insulation
            'max': 150,   # €150 for premium materials
            'default': 75
        },
        'montaža': {
            'min': 2500,  # €2500 for assembly work (based on actual formwork pricing)
            'max': 4500,  # €4500 for complex installations
            'default': 3725  # Based on realistic_test_v1.xlsx
        },
        'građevina': {
            'min': 1200,  # €1200 for basic construction work (based on actual data)
            'max': 40000, # €40000 for specialized concrete work (realistic_test_v1.xlsx)
            'default': 9500  # Average from professional specification
        },
        'vodovodne_instalacije': {
            'min': 535,   # €535 for drainage channels (actual data)
            'max': 1700,  # €1700 for complex PVC pipe systems
            'default': 1100  # Average from realistic_test_v1.xlsx
        },
        'infrastruktura': {
            'min': 500,   # €500 for infrastructure
            'max': 5000,  # €5000 for major works
            'default': 1500
        },
        'demontaža': {
            'min': 20,    # €20 for basic demolition (actual data)
            'max': 5000,  # €5000 for complex waste transport
            'default': 1900  # Average from realistic_test_v1.xlsx
        },
        'transport': {
            'min': 30,    # €30 for transport
            'max': 200,   # €200 for heavy transport
            'default': 80
        },
        'ostalo': {
            'min': 100,   # €100 for miscellaneous
            'max': 600,   # €600 for complex tasks
            'default': 250
        }
    }
    
    # Realistic project sizes (based on actual Serbian construction specifications)
    PROJECT_SIZES = {
        'small': {
            'total_range': (50000, 150000),    # €50k - €150k
            'description': 'Small residential renovation'
        },
        'medium': {
            'total_range': (150000, 500000),   # €150k - €500k
            'description': 'Medium commercial project'
        },
        'large': {
            'total_range': (500000, 1500000),  # €500k - €1.5M (like realistic_test_v1.xlsx)
            'description': 'Large infrastructure project'
        }
    }
    
    # Business parameters
    MARGIN_RANGES = {
        'low_risk': 0.12,     # 12% margin for low-risk items
        'medium_risk': 0.18,  # 18% margin for medium-risk items
        'high_risk': 0.25     # 25% margin for high-risk items
    }
    
    VAT_RATE = 0.20  # 20% VAT (standard EU rate)
    
    # Demo project templates (based on actual Serbian construction specifications)
    DEMO_PROJECTS = {
        'infrastructure_project': {
            'name': 'Infrastructure Development Project',
            'total_estimate': 1008820,  # €1,008,820 (matches realistic_test_v1.xlsx)
            'items': [
                {'category': 'vodovodne_instalacije', 'description': 'PVC pipes Ø150mm with cement coating installation', 'quantity': 220, 'unit': 'm'},
                {'category': 'građevina', 'description': 'Manual terrain excavation to specified depth', 'quantity': 2.5, 'unit': 'm³'},
                {'category': 'demontaža', 'description': 'Debris removal from construction site', 'quantity': 2.5, 'unit': 'loads'},
                {'category': 'građevina', 'description': 'Brick shaft construction 1m x 1m', 'quantity': 12, 'unit': 'pcs'},
                {'category': 'montaža', 'description': 'Foundation formwork with rubber boards', 'quantity': 3, 'unit': 'm²'},
                {'category': 'građevina', 'description': 'Concrete 1:2:4 mixed with vibrator', 'quantity': 7.5, 'unit': 'm³'},
                {'category': 'vodovodne_instalacije', 'description': 'Concrete drainage channels Ø9"', 'quantity': 63, 'unit': 'm'},
                {'category': 'građevina', 'description': 'Concrete drainage construction 300mm wide', 'quantity': 38, 'unit': 'm'}
            ]
        },
        'office_renovation': {
            'name': 'Office Building Renovation',
            'total_estimate': 250000,  # €250,000
            'items': [
                {'category': 'elektro', 'description': 'LED lighting system installation', 'quantity': 45, 'unit': 'fixtures'},
                {'category': 'mehanika', 'description': 'HVAC system upgrade', 'quantity': 1, 'unit': 'system'},
                {'category': 'građevina', 'description': 'Interior wall modifications', 'quantity': 25, 'unit': 'm²'},
                {'category': 'montaža', 'description': 'Suspended ceiling installation', 'quantity': 50, 'unit': 'm²'},
                {'category': 'demontaža', 'description': 'Old installation removal', 'quantity': 100, 'unit': 'm²'}
            ]
        },
        'residential_house': {
            'name': 'New Residential House Construction',
            'total_estimate': 650000,  # €650,000
            'items': [
                {'category': 'građevina', 'description': 'Foundation and concrete structural work', 'quantity': 15, 'unit': 'm³'},
                {'category': 'elektro', 'description': 'Complete electrical installation', 'quantity': 1, 'unit': 'house'},
                {'category': 'mehanika', 'description': 'Heat pump system installation', 'quantity': 1, 'unit': 'system'},
                {'category': 'vodovodne_instalacije', 'description': 'Plumbing and drainage system', 'quantity': 80, 'unit': 'm'},
                {'category': 'montaža', 'description': 'Roof construction and assembly', 'quantity': 120, 'unit': 'm²'},
                {'category': 'demontaža', 'description': 'Site preparation and clearing', 'quantity': 200, 'unit': 'm²'}
            ]
        }
    }

def apply_realistic_amounts_to_file(file_path: str, project_type: str = 'office_renovation'):
    """Apply realistic amounts to an existing agent file"""
    
    config = RealisticAmountsConfig()
    project = config.DEMO_PROJECTS[project_type]
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace currency references
    content = content.replace('RSD', config.CURRENCY)
    content = content.replace('din', config.CURRENCY_SYMBOL)
    
    # Update demo data creation function
    realistic_demo_data = f'''
def create_realistic_test_excel():
    """Create a realistic test Excel file with proper construction amounts"""
    import pandas as pd
    
    # {project['name']} - Estimated Total: {config.CURRENCY_SYMBOL}{project['total_estimate']:,}
    test_data = {{
        'BR.': list(range(1, len({project['items']}) + 1)),
        'OPIS POZICIJE': [item['description'] for item in {project['items']}],
        'J. MERE': [item['unit'] for item in {project['items']}],
        'KOL.': [item['quantity'] for item in {project['items']}],
        'J. CENA': [],  # Will be calculated
        'CENA': []      # Will be calculated
    }}
    
    # Calculate realistic prices
    unit_prices = []
    total_prices = []
    
    for item in {project['items']}:
        category = item['category']
        price_config = {config.REALISTIC_UNIT_PRICES}[category]
        
        # Use default price with some variation
        base_price = price_config['default']
        variation = base_price * 0.15  # ±15% variation
        import random
        unit_price = base_price + random.uniform(-variation, variation)
        
        total_price = unit_price * item['quantity']
        
        unit_prices.append(round(unit_price, 2))
        total_prices.append(round(total_price, 2))
    
    test_data['J. CENA'] = unit_prices
    test_data['CENA'] = total_prices
    
    df = pd.DataFrame(test_data)
    test_file = "realistic_construction_spec.xlsx"
    df.to_excel(test_file, index=False)
    
    print(f"✅ Realistic test Excel file created: {{test_file}}")
    print(f"📊 Project: {project['name']}")
    print(f"💰 Estimated Total: {config.CURRENCY_SYMBOL}{project['total_estimate']:,}")
    print(f"📋 Items: {{len({project['items']})}} construction items")
    
    return test_file
'''
    
    # Replace the existing create_test_excel function
    import re
    pattern = r'def create_test_excel\(\):.*?return test_file'
    content = re.sub(pattern, realistic_demo_data.strip(), content, flags=re.DOTALL)
    
    # Update margin calculation to use realistic values
    margin_update = f'''
    # Enhanced margin calculation with realistic rates
    def _calculate_realistic_margin(self, category: str, complexity: int = 3):
        """Calculate realistic margin based on category and complexity"""
        base_margins = {config.MARGIN_RANGES}
        
        if complexity <= 2:
            return base_margins['low_risk']
        elif complexity <= 3:
            return base_margins['medium_risk']
        else:
            return base_margins['high_risk']
'''
    
    # Add the margin calculation method
    content += margin_update
    
    # Write back to file
    backup_path = file_path + '.backup'
    if not Path(backup_path).exists():
        # Create backup
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(open(file_path, 'r').read())
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Updated {file_path} with realistic amounts")
    print(f"💰 Currency: {config.CURRENCY}")
    print(f"📈 Price range: {config.CURRENCY_SYMBOL}30 - {config.CURRENCY_SYMBOL}5,000 per unit")
    print(f"🏗️ Project type: {project['name']}")

def create_realistic_demo_files():
    """Create realistic demo files for all project types"""
    
    config = RealisticAmountsConfig()
    
    for project_name, project_data in config.DEMO_PROJECTS.items():
        # Create Excel file for each project type
        import pandas as pd
        import random
        
        test_data = {
            'BR.': list(range(1, len(project_data['items']) + 1)),
            'OPIS POZICIJE': [item['description'] for item in project_data['items']],
            'J. MERE': [item['unit'] for item in project_data['items']],
            'KOL.': [item['quantity'] for item in project_data['items']],
            'J. CENA': [],
            'CENA': []
        }
        
        # Calculate realistic prices
        unit_prices = []
        total_prices = []
        
        for item in project_data['items']:
            category = item['category']
            price_config = config.REALISTIC_UNIT_PRICES[category]
            
            # Use default price with realistic variation
            base_price = price_config['default']
            variation = base_price * 0.2  # ±20% variation
            unit_price = base_price + random.uniform(-variation, variation)
            
            total_price = unit_price * item['quantity']
            
            unit_prices.append(round(unit_price, 2))
            total_prices.append(round(total_price, 2))
        
        test_data['J. CENA'] = unit_prices
        test_data['CENA'] = total_prices
        
        df = pd.DataFrame(test_data)
        filename = f"realistic_{project_name}_spec.xlsx"
        df.to_excel(filename, index=False)
        
        print(f"✅ Created: {filename}")
        print(f"   📊 {project_data['name']}")
        print(f"   💰 Estimated: {config.CURRENCY_SYMBOL}{project_data['total_estimate']:,}")
        print(f"   📋 Items: {len(project_data['items'])}")
        print()

def main():
    """Main function to update files with realistic amounts"""
    print("🏗️ Construction Industry Realistic Amounts Configuration")
    print("=" * 60)
    
    config = RealisticAmountsConfig()
    
    print("💰 Configuration Summary:")
    print(f"   Currency: {config.CURRENCY} ({config.CURRENCY_SYMBOL})")
    print(f"   Price Multiplier: {config.PRICE_MULTIPLIER}x")
    print(f"   VAT Rate: {config.VAT_RATE * 100}%")
    print()
    
    print("🏗️ Project Templates:")
    for name, project in config.DEMO_PROJECTS.items():
        print(f"   • {project['name']}: {config.CURRENCY_SYMBOL}{project['total_estimate']:,}")
    print()
    
    # Create realistic demo files
    create_realistic_demo_files()
    
    # Update existing agent files (if they exist in backup)
    agent_files = [
        'backup_old_structure/excel_parser_agent.py',
        'backup_old_structure/quote_calculator_agent.py',
        'backup_old_structure/workflow_orchestrator.py'
    ]
    
    for file_path in agent_files:
        if Path(file_path).exists():
            try:
                apply_realistic_amounts_to_file(file_path, 'office_renovation')
            except Exception as e:
                print(f"⚠️ Could not update {file_path}: {str(e)}")
    
    print("🎉 Realistic amounts configuration completed!")
    print()
    print("🚀 Next steps:")
    print("   1. Use the new realistic Excel files for demos")
    print("   2. Run: python backup_old_structure/web_frontend.py")
    print("   3. Experience realistic construction industry amounts!")

if __name__ == "__main__":
    main()