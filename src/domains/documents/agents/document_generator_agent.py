#!/usr/bin/env python3
"""
Document Generator Agent for Construction Industry
Generates professional PDF and Excel documents from quote calculations
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class DocumentTemplate:
    """Document template configuration"""
    name: str
    template_type: str  # pdf, excel, word
    template_path: Optional[str] = None
    output_format: str = "pdf"

class DocumentGeneratorAgent:
    """Generates professional documents from quote data"""
    
    def __init__(self):
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict[str, DocumentTemplate]:
        """Load document templates"""
        return {
            'standard_quote': DocumentTemplate(
                name='Standard Quote',
                template_type='excel',
                output_format='xlsx'
            ),
            'detailed_quote': DocumentTemplate(
                name='Detailed Quote with Breakdown',
                template_type='excel',
                output_format='xlsx'
            ),
            'supplier_comparison': DocumentTemplate(
                name='Supplier Price Comparison',
                template_type='excel',
                output_format='xlsx'
            )
        }
    
    def generate_documents(self, quote_data: Dict, output_folder: str = "output") -> List[str]:
        """Generate all document types for a quote"""
        logger.info("Generating quote documents...")
        
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        
        generated_files = []
        
        # Generate standard quote
        standard_file = self._generate_standard_quote(quote_data, output_path)
        if standard_file:
            generated_files.append(standard_file)
        
        # Generate detailed breakdown
        detailed_file = self._generate_detailed_quote(quote_data, output_path)
        if detailed_file:
            generated_files.append(detailed_file)
        
        # Generate supplier comparison
        comparison_file = self._generate_supplier_comparison(quote_data, output_path)
        if comparison_file:
            generated_files.append(comparison_file)
        
        logger.info(f"Generated {len(generated_files)} documents")
        return generated_files
    
    def _generate_standard_quote(self, quote_data: Dict, output_path: Path) -> Optional[str]:
        """Generate standard quote Excel document"""
        try:
            quote_id = quote_data.get('quote_id', 'QUOTE001')
            filename = f"{quote_id}_standard_quote.xlsx"
            file_path = output_path / filename
            
            # Prepare data for Excel
            items_data = []
            for item in quote_data.get('items', []):
                items_data.append({
                    'Pozicija': item.get('position', ''),
                    'Opis': item.get('description', ''),
                    'Količina': item.get('quantity', 0),
                    'J.M.': item.get('unit', ''),
                    'Jedinična cena': f"{item.get('final_unit_price', 0):,.2f} RSD",
                    'Ukupno': f"{item.get('final_total_price', 0):,.2f} RSD",
                    'Dobavljač': item.get('selected_supplier', '')
                })
            
            # Create DataFrame
            df = pd.DataFrame(items_data)
            
            # Add summary row
            summary = quote_data.get('summary', {})
            summary_row = {
                'Pozicija': '',
                'Opis': 'UKUPNO pre PDV-a:',
                'Količina': '',
                'J.M.': '',
                'Jedinična cena': '',
                'Ukupno': f"{summary.get('final_total', 0) - summary.get('tax_total', 0):,.2f} RSD",
                'Dobavljač': ''
            }
            
            tax_row = {
                'Pozicija': '',
                'Opis': 'PDV (20%):',
                'Količina': '',
                'J.M.': '',
                'Jedinična cena': '',
                'Ukupno': f"{summary.get('tax_total', 0):,.2f} RSD",
                'Dobavljač': ''
            }
            
            final_row = {
                'Pozicija': '',
                'Opis': 'UKUPNO sa PDV:',
                'Količina': '',
                'J.M.': '',
                'Jedinična cena': '',
                'Ukupno': f"{summary.get('final_total', 0):,.2f} RSD",
                'Dobavljač': ''
            }
            
            # Add summary rows
            df = pd.concat([df, pd.DataFrame([summary_row, tax_row, final_row])], ignore_index=True)
            
            # Write to Excel
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Main quote sheet
                df.to_excel(writer, sheet_name='Ponuda', index=False)
                
                # Add header info
                worksheet = writer.sheets['Ponuda']
                worksheet.insert_rows(1, 5)
                
                # Add header information
                worksheet['A1'] = f"PONUDA BR: {quote_id}"
                worksheet['A2'] = f"Datum: {datetime.now().strftime('%d.%m.%Y')}"
                worksheet['A3'] = "Konstrukcijski projekat"
                worksheet['A4'] = ""  # Empty row
                
            logger.info(f"Standard quote generated: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error generating standard quote: {str(e)}")
            return None
    
    def _generate_detailed_quote(self, quote_data: Dict, output_path: Path) -> Optional[str]:
        """Generate detailed quote with supplier breakdown"""
        try:
            quote_id = quote_data.get('quote_id', 'QUOTE001')
            filename = f"{quote_id}_detailed_quote.xlsx"
            file_path = output_path / filename
            
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Main quote sheet
                items_data = []
                for item in quote_data.get('items', []):
                    items_data.append({
                        'Pozicija': item.get('position', ''),
                        'Opis': item.get('description', ''),
                        'Količina': item.get('quantity', 0),
                        'J.M.': item.get('unit', ''),
                        'Nabavna cena': f"{item.get('best_unit_price', 0):,.2f}",
                        'Marža (%)': f"{item.get('margin_percentage', 0)*100:.1f}%",
                        'Prodajna cena': f"{item.get('final_unit_price', 0):,.2f}",
                        'Ukupno': f"{item.get('final_total_price', 0):,.2f}",
                        'Dobavljač': item.get('selected_supplier', '')
                    })
                
                df_items = pd.DataFrame(items_data)
                df_items.to_excel(writer, sheet_name='Detaljna ponuda', index=False)
                
                # Supplier breakdown sheet
                supplier_data = []
                for supplier, total in quote_data.get('supplier_breakdown', {}).items():
                    supplier_data.append({
                        'Dobavljač': supplier,
                        'Ukupno': f"{total:,.2f} RSD"
                    })
                
                df_suppliers = pd.DataFrame(supplier_data)
                df_suppliers.to_excel(writer, sheet_name='Po dobavljačima', index=False)
            
            logger.info(f"Detailed quote generated: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error generating detailed quote: {str(e)}")
            return None
    
    def _generate_supplier_comparison(self, quote_data: Dict, output_path: Path) -> Optional[str]:
        """Generate supplier price comparison document"""
        try:
            quote_id = quote_data.get('quote_id', 'QUOTE001')
            filename = f"{quote_id}_supplier_comparison.xlsx"
            file_path = output_path / filename
            
            # Create comparison data (simplified for demo)
            comparison_data = []
            for item in quote_data.get('items', []):
                comparison_data.append({
                    'Pozicija': item.get('position', ''),
                    'Opis': item.get('description', ''),
                    'Izabrani dobavljač': item.get('selected_supplier', ''),
                    'Najbolja cena': f"{item.get('best_unit_price', 0):,.2f} RSD",
                    'Finalna cena': f"{item.get('final_unit_price', 0):,.2f} RSD",
                    'Status': '✅ Odabrano'
                })
            
            df_comparison = pd.DataFrame(comparison_data)
            df_comparison.to_excel(file_path, sheet_name='Poređenje dobavljača', index=False)
            
            logger.info(f"Supplier comparison generated: {file_path}")
            return str(file_path)
            
        except Exception as e:
            logger.error(f"Error generating supplier comparison: {str(e)}")
            return None
    
    def generate_summary_report(self, quote_data: Dict, output_path: str = "quote_summary.txt") -> str:
        """Generate a text summary report"""
        try:
            summary = quote_data.get('summary', {})
            quote_id = quote_data.get('quote_id', 'QUOTE001')
            
            report_lines = [
                "KONSTRUKCIJSKI PROJEKAT - SAŽETAK PONUDE",
                "=" * 50,
                f"Broj ponude: {quote_id}",
                f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                "",
                "FINANSIJSKI PREGLED:",
                f"  • Neto vrednost: {summary.get('subtotal', 0):,.2f} RSD",
                f"  • Marža: {summary.get('margin_total', 0):,.2f} RSD",
                f"  • PDV (20%): {summary.get('tax_total', 0):,.2f} RSD",
                f"  • UKUPNO: {summary.get('final_total', 0):,.2f} RSD",
                "",
                "DOBAVLJAČI:",
            ]
            
            # Add supplier breakdown
            for supplier, total in quote_data.get('supplier_breakdown', {}).items():
                report_lines.append(f"  • {supplier}: {total:,.2f} RSD")
            
            report_lines.extend([
                "",
                f"STAVKE: {len(quote_data.get('items', []))} pozicija",
                "",
                "DETALJAN PREGLED:",
            ])
            
            # Add items
            for i, item in enumerate(quote_data.get('items', []), 1):
                report_lines.extend([
                    f"{i}. {item.get('description', '')}",
                    f"   Količina: {item.get('quantity', 0)} {item.get('unit', '')}",
                    f"   Cena: {item.get('final_unit_price', 0):,.2f} RSD/{item.get('unit', '')}",
                    f"   Dobavljač: {item.get('selected_supplier', '')}",
                    ""
                ])
            
            # Write report
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            logger.info(f"Summary report generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating summary report: {str(e)}")
            return ""

def main():
    """Test the Document Generator Agent"""
    print("📄 Document Generator Agent Test")
    
    # Demo quote data
    demo_quote = {
        'quote_id': 'DEMO001',
        'summary': {
            'subtotal': 10000.0,
            'margin_total': 1500.0,
            'tax_total': 2300.0,
            'final_total': 13800.0
        },
        'supplier_breakdown': {
            'HVAC Sistem': 5000.0,
            'Elektro Plus': 3500.0
        },
        'items': [
            {
                'position': '1',
                'description': 'Split klima uređaj',
                'quantity': 5,
                'unit': 'kom',
                'best_unit_price': 400.0,
                'margin_percentage': 0.15,
                'final_unit_price': 460.0,
                'final_total_price': 2300.0,
                'selected_supplier': 'HVAC Sistem'
            }
        ]
    }
    
    agent = DocumentGeneratorAgent()
    files = agent.generate_documents(demo_quote, "demo_output")
    
    print(f"\nGenerated {len(files)} documents:")
    for file_path in files:
        print(f"  📄 {file_path}")

if __name__ == "__main__":
    main()
