#!/usr/bin/env python3
"""
Response Parser Agent for Construction Industry
Parses supplier responses from emails and PDFs to extract prices
"""

import re
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import time

logger = logging.getLogger(__name__)

@dataclass
class SupplierResponse:
    """Parsed supplier response"""
    supplier_name: str
    request_id: str
    response_type: str  # email, pdf, api
    received_timestamp: str
    items: List[Dict]  # List of items with prices
    total_value: Optional[float] = None
    confidence_score: float = 0.0

@dataclass
class PriceItem:
    """Individual price item from response"""
    position: str
    description: str
    unit_price: float
    quantity: float
    total_price: float
    unit: str
    confidence: float

class ResponseParserAgent:
    """Parses supplier responses to extract pricing data"""
    
    def __init__(self):
        self.price_patterns = self._load_price_patterns()
        
    def _load_price_patterns(self) -> List[str]:
        """Load regex patterns for price extraction"""
        return [
            r'(\d+(?:\.\d{3})*,\d{2})\s*(?:din|rsd|€)',  # European format
            r'(\d+(?:,\d{3})*\.\d{2})\s*(?:din|rsd|€)',  # US format
            r'(\d+(?:\s\d{3})*,\d{2})',  # Space-separated thousands
            r'(\d+,\d{2})',  # Simple decimal comma
            r'(\d+\.\d{2})',  # Simple decimal dot
        ]
    
    def parse_responses(self, response_files: List[str]) -> List[SupplierResponse]:
        """Parse multiple supplier response files"""
        logger.info(f"Parsing {len(response_files)} supplier responses...")
        
        parsed_responses = []
        
        for file_path in response_files:
            try:
                response = self._parse_single_response(file_path)
                if response:
                    parsed_responses.append(response)
            except Exception as e:
                logger.error(f"Failed to parse {file_path}: {str(e)}")
        
        logger.info(f"Successfully parsed {len(parsed_responses)} responses")
        return parsed_responses
    
    def _parse_single_response(self, file_path: str) -> Optional[SupplierResponse]:
        """Parse a single response file"""
        path = Path(file_path)
        
        if not path.exists():
            logger.warning(f"Response file not found: {file_path}")
            return None
        
        # For demo purposes, simulate parsing different file types
        if path.suffix.lower() == '.json':
            return self._parse_json_response(file_path)
        elif path.suffix.lower() == '.txt':
            return self._parse_text_response(file_path)
        elif path.suffix.lower() == '.pdf':
            return self._parse_pdf_response(file_path)
        else:
            logger.warning(f"Unsupported file type: {path.suffix}")
            return None
    
    def _parse_json_response(self, file_path: str) -> Optional[SupplierResponse]:
        """Parse JSON response (API responses)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extract supplier info
            supplier_name = data.get('supplier_name', 'Unknown')
            request_id = data.get('request_id', 'Unknown')
            
            # Parse items
            items = []
            for item_data in data.get('items', []):
                price_item = {
                    'position': item_data.get('position', ''),
                    'description': item_data.get('description', ''),
                    'unit_price': float(item_data.get('unit_price', 0)),
                    'quantity': float(item_data.get('quantity', 0)),
                    'total_price': float(item_data.get('total_price', 0)),
                    'unit': item_data.get('unit', ''),
                    'confidence': 0.95  # High confidence for structured data
                }
                items.append(price_item)
            
            return SupplierResponse(
                supplier_name=supplier_name,
                request_id=request_id,
                response_type='api',
                received_timestamp=str(time.time()),
                items=items,
                confidence_score=0.95
            )
            
        except Exception as e:
            logger.error(f"Error parsing JSON response: {str(e)}")
            return None
    
    def _parse_text_response(self, file_path: str) -> Optional[SupplierResponse]:
        """Parse text/email response"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Demo parsing - extract prices using patterns
            items = []
            lines = content.split('\n')
            
            current_item = {}
            for line in lines:
                line = line.strip()
                
                # Look for item descriptions
                if any(keyword in line.lower() for keyword in ['pozicija', 'stavka', 'item']):
                    if current_item:
                        items.append(current_item)
                    current_item = {'description': line, 'confidence': 0.7}
                
                # Look for prices
                for pattern in self.price_patterns:
                    matches = re.findall(pattern, line)
                    if matches and current_item:
                        price_str = matches[0]
                        try:
                            # Convert to float (handle European format)
                            price = float(price_str.replace('.', '').replace(',', '.'))
                            current_item['unit_price'] = price
                            current_item['total_price'] = price
                            current_item['quantity'] = 1.0
                            current_item['unit'] = 'kom'
                        except ValueError:
                            continue
            
            if current_item:
                items.append(current_item)
            
            return SupplierResponse(
                supplier_name="Email Supplier",
                request_id="EMAIL_REQ",
                response_type='email',
                received_timestamp=str(time.time()),
                items=items,
                confidence_score=0.7
            )
            
        except Exception as e:
            logger.error(f"Error parsing text response: {str(e)}")
            return None
    
    def _parse_pdf_response(self, file_path: str) -> Optional[SupplierResponse]:
        """Parse PDF response (would use OCR in real implementation)"""
        # For demo, return a mock response
        logger.info(f"📄 [DEMO] Parsing PDF: {file_path}")
        
        demo_items = [
            {
                'position': '1',
                'description': 'PDF Item 1',
                'unit_price': 100.0,
                'quantity': 1.0,
                'total_price': 100.0,
                'unit': 'kom',
                'confidence': 0.6
            }
        ]
        
        return SupplierResponse(
            supplier_name="PDF Supplier",
            request_id="PDF_REQ",
            response_type='pdf',
            received_timestamp=str(time.time()),
            items=demo_items,
            confidence_score=0.6
        )
    
    def create_price_comparison(self, responses: List[SupplierResponse]) -> Dict[str, Dict]:
        """Create price comparison across suppliers"""
        comparison = {}
        
        # Group by item description/position
        for response in responses:
            for item in response.items:
                key = f"{item.get('position', '')}_{item.get('description', '')}"
                
                if key not in comparison:
                    comparison[key] = {
                        'description': item.get('description'),
                        'suppliers': {}
                    }
                
                comparison[key]['suppliers'][response.supplier_name] = {
                    'unit_price': item.get('unit_price'),
                    'total_price': item.get('total_price'),
                    'confidence': item.get('confidence')
                }
        
        return comparison
    
    def export_parsed_responses(self, responses: List[SupplierResponse], output_path: str):
        """Export parsed responses to JSON"""
        export_data = []
        
        for response in responses:
            export_data.append({
                'supplier_name': response.supplier_name,
                'request_id': response.request_id,
                'response_type': response.response_type,
                'received_timestamp': response.received_timestamp,
                'items': response.items,
                'total_value': response.total_value,
                'confidence_score': response.confidence_score
            })
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Parsed responses exported to: {output_path}")

def main():
    """Test the Response Parser Agent"""
    print("📥 Response Parser Agent Test")
    
    # Create demo response files
    demo_json = {
        'supplier_name': 'Demo Supplier',
        'request_id': 'REQ001',
        'items': [
            {
                'position': '1',
                'description': 'Split klima uređaj',
                'unit_price': 500.0,
                'quantity': 5,
                'total_price': 2500.0,
                'unit': 'kom'
            }
        ]
    }
    
    with open('demo_response.json', 'w') as f:
        json.dump(demo_json, f)
    
    agent = ResponseParserAgent()
    responses = agent.parse_responses(['demo_response.json'])
    
    print(f"\nParsed {len(responses)} responses:")
    for response in responses:
        print(f"  • {response.supplier_name}: {len(response.items)} items")

if __name__ == "__main__":
    main()
