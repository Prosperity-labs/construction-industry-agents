#!/usr/bin/env python3
"""
Quote Calculator Agent for Construction Industry
Calculates optimal quotes based on supplier responses and business rules
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import statistics

logger = logging.getLogger(__name__)

@dataclass
class QuoteItem:
    """Single item in the final quote"""
    position: str
    description: str
    quantity: float
    unit: str
    best_unit_price: float
    total_price: float
    selected_supplier: str
    margin_percentage: float
    final_unit_price: float
    final_total_price: float

@dataclass
class QuoteCalculation:
    """Complete quote calculation result"""
    quote_id: str
    items: List[QuoteItem]
    subtotal: float
    margin_total: float
    tax_total: float
    final_total: float
    supplier_breakdown: Dict[str, float]
    calculation_timestamp: str

class QuoteCalculatorAgent:
    """Calculates optimal quotes from supplier responses"""
    
    def __init__(self, default_margin: float = 0.15, tax_rate: float = 0.20):
        self.default_margin = default_margin  # 15% default margin
        self.tax_rate = tax_rate  # 20% VAT
        self.category_margins = {
            'mehanika': 0.18,
            'elektro': 0.16, 
            'izolacija': 0.14,
            'montaža': 0.20,
            'građevina': 0.12,
            'vodovodne_instalacije': 0.17,
            'infrastruktura': 0.15,
            'demontaža': 0.25,
            'transport': 0.10,
            'ostalo': 0.15
        }
    
    def calculate_quote(self, 
                       original_items: List[Dict], 
                       supplier_responses: List[Dict],
                       quote_id: str = "QUOTE001") -> QuoteCalculation:
        """Calculate final quote from original items and supplier responses"""
        logger.info(f"Calculating quote {quote_id} for {len(original_items)} items...")
        
        quote_items = []
        supplier_totals = {}
        
        for original_item in original_items:
            quote_item = self._calculate_item_quote(original_item, supplier_responses)
            if quote_item:
                quote_items.append(quote_item)
                
                # Track supplier totals
                supplier = quote_item.selected_supplier
                if supplier not in supplier_totals:
                    supplier_totals[supplier] = 0.0
                supplier_totals[supplier] += quote_item.final_total_price
        
        # Calculate totals
        subtotal = sum(item.total_price for item in quote_items)
        margin_total = sum(item.final_total_price - item.total_price for item in quote_items)
        final_total_before_tax = sum(item.final_total_price for item in quote_items)
        tax_total = final_total_before_tax * self.tax_rate
        final_total = final_total_before_tax + tax_total
        
        calculation = QuoteCalculation(
            quote_id=quote_id,
            items=quote_items,
            subtotal=subtotal,
            margin_total=margin_total,
            tax_total=tax_total,
            final_total=final_total,
            supplier_breakdown=supplier_totals,
            calculation_timestamp=str(time.time()) if 'time' in globals() else "demo"
        )
        
        logger.info(f"Quote calculated: {len(quote_items)} items, total: {final_total:,.2f} RSD")
        return calculation
    
    def _calculate_item_quote(self, original_item: Dict, supplier_responses: List[Dict]) -> Optional[QuoteItem]:
        """Calculate quote for a single item"""
        position = original_item.get('position_number', '')
        description = original_item.get('description', '')
        quantity = float(original_item.get('quantity', 0))
        unit = original_item.get('unit', '')
        category = original_item.get('category', 'ostalo')
        
        # Find best price from supplier responses
        best_price = None
        best_supplier = "No supplier found"
        
        prices = []
        for response in supplier_responses:
            for item in response.get('items', []):
                # Match by position or description similarity
                if (position and item.get('position') == position) or                    (description and self._similarity_match(description, item.get('description', ''))):
                    unit_price = item.get('unit_price', 0)
                    if unit_price > 0:
                        prices.append((unit_price, response.get('supplier_name', 'Unknown')))
        
        if not prices:
            logger.warning(f"No prices found for item: {position} - {description}")
            return None
        
        # Select best price (lowest for now, could be more sophisticated)
        best_price, best_supplier = min(prices, key=lambda x: x[0])
        
        # Calculate margins
        margin_percentage = self.category_margins.get(category, self.default_margin)
        final_unit_price = best_price * (1 + margin_percentage)
        total_price = best_price * quantity
        final_total_price = final_unit_price * quantity
        
        return QuoteItem(
            position=position,
            description=description,
            quantity=quantity,
            unit=unit,
            best_unit_price=best_price,
            total_price=total_price,
            selected_supplier=best_supplier,
            margin_percentage=margin_percentage,
            final_unit_price=final_unit_price,
            final_total_price=final_total_price
        )
    
    def _similarity_match(self, desc1: str, desc2: str, threshold: float = 0.6) -> bool:
        """Simple similarity matching for descriptions"""
        if not desc1 or not desc2:
            return False
        
        # Simple word overlap method
        words1 = set(desc1.lower().split())
        words2 = set(desc2.lower().split())
        
        if not words1 or not words2:
            return False
        
        overlap = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        similarity = overlap / union if union > 0 else 0
        return similarity >= threshold
    
    def optimize_supplier_selection(self, calculation: QuoteCalculation) -> QuoteCalculation:
        """Optimize supplier selection to minimize total suppliers"""
        logger.info("Optimizing supplier selection...")
        
        # Group items by supplier
        supplier_groups = {}
        for item in calculation.items:
            supplier = item.selected_supplier
            if supplier not in supplier_groups:
                supplier_groups[supplier] = []
            supplier_groups[supplier].append(item)
        
        # For now, keep current selection (could implement more sophisticated optimization)
        logger.info(f"Current supplier distribution: {len(supplier_groups)} suppliers")
        for supplier, items in supplier_groups.items():
            total = sum(item.final_total_price for item in items)
            logger.info(f"  • {supplier}: {len(items)} items, {total:,.2f} RSD")
        
        return calculation
    
    def export_quote(self, calculation: QuoteCalculation, output_path: str):
        """Export quote calculation to JSON"""
        export_data = {
            'quote_id': calculation.quote_id,
            'calculation_timestamp': calculation.calculation_timestamp,
            'summary': {
                'subtotal': calculation.subtotal,
                'margin_total': calculation.margin_total,
                'tax_total': calculation.tax_total,
                'final_total': calculation.final_total
            },
            'supplier_breakdown': calculation.supplier_breakdown,
            'items': [
                {
                    'position': item.position,
                    'description': item.description,
                    'quantity': item.quantity,
                    'unit': item.unit,
                    'best_unit_price': item.best_unit_price,
                    'margin_percentage': item.margin_percentage,
                    'final_unit_price': item.final_unit_price,
                    'final_total_price': item.final_total_price,
                    'selected_supplier': item.selected_supplier
                }
                for item in calculation.items
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Quote exported to: {output_path}")

def main():
    """Test the Quote Calculator Agent"""
    print("🧮 Quote Calculator Agent Test")
    
    # Demo data
    demo_items = [
        {
            'position_number': '1',
            'description': 'Split klima uređaj',
            'quantity': 5,
            'unit': 'kom',
            'category': 'mehanika'
        }
    ]
    
    demo_responses = [
        {
            'supplier_name': 'HVAC Sistem',
            'items': [
                {
                    'position': '1',
                    'description': 'Split klima uređaj',
                    'unit_price': 500.0
                }
            ]
        },
        {
            'supplier_name': 'Klima Plus',
            'items': [
                {
                    'position': '1', 
                    'description': 'Split klima uređaj',
                    'unit_price': 480.0
                }
            ]
        }
    ]
    
    agent = QuoteCalculatorAgent()
    calculation = agent.calculate_quote(demo_items, demo_responses)
    
    print(f"\nQuote calculated:")
    print(f"  Items: {len(calculation.items)}")
    print(f"  Subtotal: {calculation.subtotal:,.2f} RSD")
    print(f"  Final total: {calculation.final_total:,.2f} RSD")

if __name__ == "__main__":
    main()
