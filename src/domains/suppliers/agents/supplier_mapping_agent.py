#!/usr/bin/env python3
"""
Supplier Mapping Agent for Construction Industry
Maps construction items to appropriate suppliers based on category and location
"""

import json
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class Supplier:
    """Supplier information"""
    name: str
    category: str
    contact_email: str
    contact_phone: str
    location: str
    rating: float = 0.0
    specialties: List[str] = None
    
    def __post_init__(self):
        if self.specialties is None:
            self.specialties = []

@dataclass
class SupplierMatch:
    """Supplier match result"""
    supplier: Supplier
    confidence: float
    matching_categories: List[str]

class SupplierMappingAgent:
    """Maps construction items to suppliers"""
    
    def __init__(self):
        self.suppliers_db = self._load_suppliers_database()
        
    def _load_suppliers_database(self) -> List[Supplier]:
        """Load suppliers database (demo data for now)"""
        demo_suppliers = [
            Supplier("HVAC Sistem doo", "mehanika", "office@hvacsistem.rs", "+381 11 123 4567", "Beograd"),
            Supplier("Elektro Montaža", "elektro", "info@elektromontaza.rs", "+381 21 234 5678", "Novi Sad"),
            Supplier("Izolacija Plus", "izolacija", "prodaja@izolacijaplus.rs", "+381 18 345 6789", "Niš"),
            Supplier("Građevinski Materijal", "građevina", "info@gradmat.rs", "+381 11 456 7890", "Beograd"),
            Supplier("Opšti Dobavljač", "ostalo", "kontakt@opsti.rs", "+381 11 567 8901", "Beograd")
        ]
        return demo_suppliers
    
    def map_suppliers(self, items: List[Dict]) -> Dict[str, List[SupplierMatch]]:
        """Map items to appropriate suppliers"""
        logger.info(f"Mapping {len(items)} items to suppliers...")
        
        mappings = {}
        
        for item in items:
            category = item.get('category', 'ostalo')
            matches = self._find_suppliers_for_category(category)
            mappings[item.get('position_number', 'unknown')] = matches
            
        logger.info(f"Found supplier mappings for {len(mappings)} items")
        return mappings
    
    def _find_suppliers_for_category(self, category: str) -> List[SupplierMatch]:
        """Find suppliers for a specific category"""
        matches = []
        
        for supplier in self.suppliers_db:
            confidence = 0.0
            matching_categories = []
            
            # Direct category match
            if supplier.category == category:
                confidence = 0.9
                matching_categories.append(category)
            # Check specialties
            elif category in supplier.specialties:
                confidence = 0.7
                matching_categories.append(category)
            # General supplier fallback
            elif supplier.category == 'ostalo':
                confidence = 0.3
                matching_categories.append('ostalo')
            
            if confidence > 0:
                matches.append(SupplierMatch(
                    supplier=supplier,
                    confidence=confidence,
                    matching_categories=matching_categories
                ))
        
        # Sort by confidence
        matches.sort(key=lambda x: x.confidence, reverse=True)
        return matches[:3]  # Return top 3 matches
    
    def export_supplier_mappings(self, mappings: Dict[str, List[SupplierMatch]], output_path: str):
        """Export supplier mappings to JSON"""
        export_data = {}
        
        for item_id, matches in mappings.items():
            export_data[item_id] = [
                {
                    'supplier': asdict(match.supplier),
                    'confidence': match.confidence,
                    'matching_categories': match.matching_categories
                }
                for match in matches
            ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Supplier mappings exported to: {output_path}")

def main():
    """Test the Supplier Mapping Agent"""
    print("🏭 Supplier Mapping Agent Test")
    
    # Demo items
    demo_items = [
        {'position_number': '1', 'category': 'mehanika', 'description': 'HVAC sistem'},
        {'position_number': '2', 'category': 'elektro', 'description': 'LED rasveta'},
        {'position_number': '3', 'category': 'izolacija', 'description': 'Toplotna izolacija'}
    ]
    
    agent = SupplierMappingAgent()
    mappings = agent.map_suppliers(demo_items)
    
    for item_id, matches in mappings.items():
        print(f"\nItem {item_id}:")
        for match in matches:
            print(f"  • {match.supplier.name} ({match.confidence:.1f})")

if __name__ == "__main__":
    main()
