#!/usr/bin/env python3
"""
Excel Parser Agent for Construction Specifications
Designed to parse Serbian construction Excel files and extract structured data

Usage with Claude Code:
1. Save this file as excel_parser_agent.py
2. Create test Excel files or use your own
3. Run: python excel_parser_agent.py
"""

import pandas as pd
import openpyxl
from typing import Dict, List, Optional, Tuple, Any
import re
from dataclasses import dataclass, asdict
import json
import sys
from pathlib import Path
import logging
import openai
import os
from concurrent.futures import ThreadPoolExecutor
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ConstructionItem:
    """Data class for construction specification items"""
    position_number: str
    description: str
    unit: str
    quantity: float
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    category: Optional[str] = None
    supplier_type: Optional[str] = None
    confidence_score: Optional[float] = None
    complexity: Optional[int] = None
    material_vs_labor: Optional[str] = None
    technical_specs: Optional[str] = None
    risk_level: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

class LLMEnhancementAgent:
    """
    Agent for enhancing construction item analysis using OpenAI LLM
    """
    
    def __init__(self, api_key: Optional[str] = None, enable_llm: bool = True):
        self.enable_llm = enable_llm
        
        if self.enable_llm:
            # Initialize OpenAI client
            self.client = openai.OpenAI(
                api_key=api_key or os.getenv('OPENAI_API_KEY')
            )
            
            if not self.client.api_key:
                logger.warning("OpenAI API key not found. LLM enhancement disabled.")
                self.enable_llm = False
        
        # Enhanced category mappings for better supplier suggestions
        self.enhanced_supplier_mapping = {
            'mehanika': 'HVAC dobavljač',
            'elektro': 'Elektro dobavljač', 
            'izolacija': 'Izolacioni materijali',
            'montaža': 'Izvođačke usluge',
            'građevina': 'Građevinski materijali',
            'vodovodne_instalacije': 'Sanitarne instalacije',
            'podovi_zidovi': 'Završni radovi',
            'krov_fasada': 'Krovni i fasadni radovi',
            'infrastruktura': 'Infrastrukturni radovi',
            'demontaža': 'Demolicija i uklanjanje',
            'transport': 'Transport i logistika',
            'ostalo': 'Opšti dobavljač'
        }
    
    def enhance_items(self, items: List[ConstructionItem]) -> List[ConstructionItem]:
        """
        Enhance construction items with LLM analysis
        """
        if not self.enable_llm or not items:
            logger.info("LLM enhancement skipped")
            return items
        
        logger.info(f"Enhancing {len(items)} items with OpenAI LLM...")
        
        try:
            # Process items in batches for efficiency
            batch_size = 10
            enhanced_items = []
            
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                enhanced_batch = self._process_batch(batch)
                enhanced_items.extend(enhanced_batch)
                
                # Rate limiting
                if i + batch_size < len(items):
                    time.sleep(1)
            
            logger.info("LLM enhancement completed successfully")
            return enhanced_items
            
        except Exception as e:
            logger.error(f"LLM enhancement failed: {str(e)}")
            logger.info("Falling back to rule-based categorization")
            return items
    
    def _process_batch(self, items: List[ConstructionItem]) -> List[ConstructionItem]:
        """Process a batch of items with OpenAI"""
        
        # Prepare descriptions for analysis
        descriptions = []
        for i, item in enumerate(items):
            descriptions.append(f"{i+1}. {item.description}")
        
        prompt = self._create_analysis_prompt(descriptions)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective and fast
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in Serbian construction and building projects. Analyze construction specifications and provide structured categorization."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=2000
            )
            
            # Parse LLM response and apply to items
            analysis = self._parse_llm_response(response.choices[0].message.content)
            return self._apply_enhancements(items, analysis)
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            return items
    
    def _create_analysis_prompt(self, descriptions: List[str]) -> str:
        """Create a structured prompt for LLM analysis"""
        
        descriptions_text = "\n".join(descriptions)
        
        return f"""
Analyze these Serbian construction project items and provide categorization:

AVAILABLE CATEGORIES:
- mehanika: HVAC, heating, cooling, ventilation, pipes, mechanical systems
- elektro: electrical installations, wiring, lighting, power systems
- izolacija: insulation, thermal protection, sound proofing
- montaža: installation, assembly, mounting work
- građevina: construction, concrete, masonry, structural work
- vodovodne_instalacije: plumbing, water supply, drainage, sewage
- infrastruktura: roads, utilities, site preparation, excavation
- demontaža: demolition, removal, dismantling
- transport: material transport, waste removal, logistics
- ostalo: other/miscellaneous items

CONSTRUCTION ITEMS:
{descriptions_text}

For each item, provide ONLY a JSON response with this exact format:
{{
  "1": {{
    "category": "category_name",
    "complexity": 3,
    "material_vs_labor": "mixed",
    "risk_level": "medium",
    "technical_specs": "brief key specifications"
  }},
  "2": {{ ... }}
}}

GUIDELINES:
- complexity: 1-5 (1=simple, 5=very complex)
- material_vs_labor: "material", "labor", "mixed"
- risk_level: "nizak", "srednji", "visok" 
- technical_specs: kratak opis ključnih specifikacija (max 50 karaktera, na srpskom)
- Budite precizni i konzistentni
- Fokusiraj se na GLAVNU aktivnost opisanu
- Odgovori SAMO na srpskom jeziku
"""
    
    def _parse_llm_response(self, response_text: str) -> Dict[str, Dict]:
        """Parse LLM response into structured data"""
        try:
            # Extract JSON from response
            response_text = response_text.strip()
            
            # Find JSON block
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                logger.warning("No JSON found in LLM response")
                return {}
            
            json_text = response_text[start_idx:end_idx]
            analysis = json.loads(json_text)
            
            logger.info(f"Successfully parsed LLM analysis for {len(analysis)} items")
            return analysis
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return {}
    
    def _apply_enhancements(self, items: List[ConstructionItem], analysis: Dict[str, Dict]) -> List[ConstructionItem]:
        """Apply LLM analysis to construction items"""
        
        for i, item in enumerate(items):
            item_key = str(i + 1)
            
            if item_key in analysis:
                enhancement = analysis[item_key]
                
                # Apply enhancements
                item.category = enhancement.get('category', item.category)
                item.complexity = enhancement.get('complexity')
                item.material_vs_labor = enhancement.get('material_vs_labor')
                item.risk_level = enhancement.get('risk_level')
                item.technical_specs = enhancement.get('technical_specs')
                
                # Update supplier type based on enhanced category
                item.supplier_type = self.enhanced_supplier_mapping.get(
                    item.category, 'Opšti dobavljač'
                )
                
                # Boost confidence if LLM enhanced
                if item.confidence_score:
                    item.confidence_score = min(item.confidence_score + 0.15, 1.0)
                
                logger.debug(f"Enhanced item {i+1}: {item.category}")
        
        return items

class ExcelParserAgent:
    """
    Agent for parsing Serbian construction Excel specifications
    Handles various Excel formats and extracts structured data
    """
    
    def __init__(self, debug: bool = False, enable_llm: bool = True, openai_api_key: Optional[str] = None):
        self.debug = debug
        self.enable_llm = enable_llm
        
        # Initialize LLM enhancement agent
        self.llm_agent = LLMEnhancementAgent(
            api_key=openai_api_key, 
            enable_llm=enable_llm
        )
        
        # Serbian column headers and their variations
        self.column_mappings = {
            'position': ['br', 'br.', 'pozicija', 'redni broj', 'rbr', 'red. br.', 'r.br.', 'stavka br.', 'stavka'],
            'description': ['opis', 'opis pozicije', 'naziv', 'specifikacija', 'rada', 'opis rada', 'pozicija'],
            'unit': ['j. mere', 'j.mere', 'jm', 'jedinica mere', 'jedinica', 'um', 'j. mera', 'mera', 'jed.'],
            'quantity': ['kol', 'kol.', 'količina', 'komada', 'količina', 'broj'],
            'unit_price': ['j. cena', 'j.cena', 'jedinična cena', 'cena po jedinici', 'j.c.', 'jed. cena', 'jedinična cena (€)', 'jedinična cena (rsd)'],
            'total_price': ['ukupno', 'ukupna cena', 'vrednost', 'uk. cena', 'uk.cena', 'ukupno (€)', 'ukupno (rsd)', 'cena']
        }
        
        # Enhanced category classification keywords
        self.category_keywords = {
            'mehanika': [
                'klima', 'grejanje', 'ventilacija', 'cevi', 'radijator', 'split', 
                'kanalice', 'hvac', 'termo', 'cooling', 'heating', 'cev', 'bakat',
                'fan-coil', 'bakarnih', 'fan coil'
            ],
            'elektro': [
                'elektro', 'kablovi', 'instalacija', 'struja', 'osvetljenje', 
                'kabel', 'žica', 'prekidač', 'utičnica', 'rasveta', 'led'
            ],
            'izolacija': [
                'izolacija', 'termo', 'mineralna vuna', 'stiropor', 'eps', 
                'toplota', 'zvuk', 'hidro', 'paropropusna', 'toplotna'
            ],
            'montaža': [
                'montaža', 'postavljanje', 'ugradnja', 'vezivanje', 'fiksiranje',
                'učvršćivanje', 'instaliranje', 'podešavanje', 'polaganje'
            ],
            'građevina': [
                'beton', 'zid', 'otvori', 'probijanje', 'rušenje', 'malter',
                'cigle', 'blok', 'AB', 'armatura', 'betoniranje', 'opeka',
                'šahte', 'izgradnja', 'poklopac'
            ],
            'vodovodne_instalacije': [
                'voda', 'kanalizacija', 'odvod', 'slavine', 'wc', 'kupatilo',
                'sanitarije', 'vodovod', 'septik', 'rušenje odvoda', 'drenažni'
            ],
            'infrastruktura': [
                'iskop', 'teren', 'gradilište', 'put', 'pristup', 'nivelacija',
                'pvc cevi', 'kanali', 'infrastructure'
            ],
            'demontaža': [
                'rušenje', 'demontaža', 'uklanjanje', 'demoliranje', 'razbijanje'
            ],
            'transport': [
                'odvoz', 'transport', 'šut', 'vozilo', 'utovar', 'prevoz'
            ]
        }
        
        # Enhanced supplier type mapping
        self.supplier_mapping = {
            'mehanika': 'HVAC dobavljač',
            'elektro': 'Elektro dobavljač', 
            'izolacija': 'Izolacioni materijali',
            'montaža': 'Izvođačke usluge',
            'građevina': 'Građevinski materijali',
            'vodovodne_instalacije': 'Sanitarne instalacije',
            'podovi_zidovi': 'Završni radovi',
            'krov_fasada': 'Krovni i fasadni radovi',
            'infrastruktura': 'Infrastrukturni radovi',
            'demontaža': 'Demolicija i uklanjanje', 
            'transport': 'Transport i logistika',
            'ostalo': 'Opšti dobavljač'
        }
    
    def parse_excel(self, file_path: str) -> List[ConstructionItem]:
        """
        Main method to parse Excel file and extract construction items
        
        Args:
            file_path: Path to Excel file
            
        Returns:
            List of ConstructionItem objects
        """
        logger.info(f"Starting to parse Excel file: {file_path}")
        
        try:
            # Check if file exists
            if not Path(file_path).exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Load Excel file
            df = self._load_excel_file(file_path)
            logger.info(f"Loaded Excel file with {len(df)} rows and {len(df.columns)} columns")
            
            if self.debug:
                print("=== RAW DATA PREVIEW ===")
                print(df.head(10))
                print("\n=== COLUMN INFO ===")
                print(f"Columns: {list(df.columns)}")
                print(f"Shape: {df.shape}")
                
                # Show first few rows as they appear
                print("\n=== FIRST 3 ROWS AS PARSED ===")
                for i in range(min(3, len(df))):
                    print(f"Row {i}: {list(df.iloc[i])}")
            
            # Find header row and column mappings
            header_row, column_map = self._find_headers(df)
            logger.info(f"Found headers at row {header_row}: {column_map}")
            
            if self.debug:
                print(f"\n=== HEADER DETECTION ===")
                print(f"Header row: {header_row}")
                print(f"Column mappings: {column_map}")
                
                # Show the actual header row
                if header_row < len(df):
                    header_values = list(df.iloc[header_row])
                    print(f"Header values: {header_values}")
                    
                    # Show mapping details
                    for field, col_idx in column_map.items():
                        if col_idx < len(header_values):
                            print(f"  {field} -> Column {col_idx}: '{header_values[col_idx]}'")
            
            # Extract data starting from header row
            items = self._extract_items(df, header_row, column_map)
            logger.info(f"Extracted {len(items)} items")
            
            # Categorize items with rule-based approach first
            for item in items:
                item.category = self._categorize_item(item.description)
                item.supplier_type = self._determine_supplier_type(item.category)
                item.confidence_score = self._calculate_confidence(item)
            
            # Enhance with LLM if enabled
            if self.enable_llm:
                logger.info("Enhancing categorization with OpenAI LLM...")
                items = self.llm_agent.enhance_items(items)
            
            logger.info(f"Successfully parsed {len(items)} construction items")
            return items
            
        except Exception as e:
            logger.error(f"Error parsing Excel file: {str(e)}")
            raise Exception(f"Error parsing Excel file: {str(e)}")
    
    def _load_excel_file(self, file_path: str) -> pd.DataFrame:
        """Load Excel file with multiple fallback methods"""
        try:
            # Try reading with openpyxl engine (recommended for .xlsx)
            df = pd.read_excel(file_path, engine='openpyxl', header=None)
            return df
        except Exception as e1:
            try:
                # Try with default engine
                df = pd.read_excel(file_path, header=None)
                return df
            except Exception as e2:
                try:
                    # Try with xlrd engine for older Excel files (.xls)
                    df = pd.read_excel(file_path, engine='xlrd', header=None)
                    return df
                except Exception as e3:
                    raise Exception(f"Could not read Excel file. Tried multiple engines. Last error: {str(e3)}")
    
    def _find_headers(self, df: pd.DataFrame) -> Tuple[int, Dict[str, int]]:
        """
        Find the header row and map columns to our expected fields
        
        Returns:
            Tuple of (header_row_index, column_mapping)
        """
        column_map = {}
        header_row = 0
        
        # Search through first 15 rows for headers
        for row_idx in range(min(15, len(df))):
            row = df.iloc[row_idx].astype(str).str.lower().str.strip()
            
            temp_map = {}
            used_columns = set()  # Track which columns we've already assigned
            
            # First pass: find exact matches and prioritize them
            for field, variations in self.column_mappings.items():
                best_match = None
                best_col_idx = None
                best_score = 0
                
                for col_idx, cell_value in enumerate(row):
                    if pd.isna(cell_value) or cell_value == 'nan' or col_idx in used_columns:
                        continue
                    
                    for var in variations:
                        if var in cell_value:
                            # Score based on how close the match is
                            score = len(var) / len(cell_value) if len(cell_value) > 0 else 0
                            if score > best_score:
                                best_score = score
                                best_match = var
                                best_col_idx = col_idx
                
                if best_col_idx is not None:
                    temp_map[field] = best_col_idx
                    used_columns.add(best_col_idx)
            
            if self.debug:
                print(f"Row {row_idx} analysis:")
                print(f"  Headers: {list(row)}")
                print(f"  Mappings found: {temp_map}")
            
            # If we found at least position and description columns, we have our header
            if 'position' in temp_map and 'description' in temp_map:
                column_map = temp_map
                header_row = row_idx
                
                # Additional validation for price columns
                if 'unit_price' in column_map and 'total_price' in column_map:
                    if column_map['unit_price'] == column_map['total_price']:
                        # Same column mapped to both - try to find a better total_price column
                        for col_idx, cell_value in enumerate(row):
                            if col_idx != column_map['unit_price'] and col_idx not in used_columns:
                                cell_lower = str(cell_value).lower()
                                if any(term in cell_lower for term in ['ukupno', 'total', 'vrednost']):
                                    column_map['total_price'] = col_idx
                                    break
                
                break
        
        if not column_map:
            # Try a more flexible approach - look for any numeric pattern in first column
            for row_idx in range(min(10, len(df))):
                first_col = str(df.iloc[row_idx, 0])
                if first_col.strip() in ['1', '1.', 'br', 'br.', 'BR', 'BR.']:
                    column_map = {
                        'position': 0,
                        'description': 1 if len(df.columns) > 1 else 0
                    }
                    header_row = row_idx
                    break
        
        if not column_map:
            raise Exception("Could not find valid headers in Excel file. Please check the file format.")
        
        return header_row, column_map
    
    def _extract_items(self, df: pd.DataFrame, header_row: int, column_map: Dict[str, int]) -> List[ConstructionItem]:
        """Extract construction items from DataFrame"""
        items = []
        
        # Start reading from row after header
        for row_idx in range(header_row + 1, len(df)):
            row = df.iloc[row_idx]
            
            # Skip empty rows
            if row.isna().all():
                continue
            
            try:
                # Extract position number
                position = str(row.iloc[column_map['position']]) if 'position' in column_map else str(row_idx)
                if position == 'nan' or not position.strip():
                    continue
                
                # Extract description
                description = str(row.iloc[column_map['description']]) if 'description' in column_map else ""
                if description == 'nan' or not description.strip():
                    continue
                
                # Skip if description looks like a header or separator
                if len(description) < 5 or description.lower() in ['opis', 'naziv', 'pozicija']:
                    continue
                
                # Extract other fields with safe defaults
                unit = str(row.iloc[column_map['unit']]) if 'unit' in column_map else ""
                unit = unit if unit != 'nan' else ""
                
                quantity = self._parse_number(row.iloc[column_map['quantity']]) if 'quantity' in column_map else 0.0
                if quantity is None:
                    quantity = 0.0
                
                unit_price = None
                if 'unit_price' in column_map:
                    unit_price = self._parse_number(row.iloc[column_map['unit_price']])
                
                total_price = None
                if 'total_price' in column_map:
                    total_price = self._parse_number(row.iloc[column_map['total_price']])
                
                # Create ConstructionItem
                item = ConstructionItem(
                    position_number=position.strip(),
                    description=description.strip(),
                    unit=unit.strip(),
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                
                # Validate and fix total price calculation if needed
                if unit_price and quantity and not total_price:
                    # Calculate total if missing
                    item.total_price = unit_price * quantity
                elif unit_price and quantity and total_price:
                    # Verify calculation and flag if inconsistent
                    calculated_total = unit_price * quantity
                    if abs(calculated_total - total_price) > 0.01:  # Allow small rounding differences
                        if self.debug:
                            print(f"Warning: Total price mismatch for item {position}")
                            print(f"  Calculated: {calculated_total:.2f} | Provided: {total_price:.2f}")
                        # Use the provided total price but add a note
                        item.total_price = total_price
                
                items.append(item)
                
            except Exception as e:
                if self.debug:
                    print(f"Warning: Could not parse row {row_idx}: {str(e)}")
                continue
        
        return items
    
    def _parse_number(self, value) -> Optional[float]:
        """Parse numeric values from Excel cells with Serbian/European formatting"""
        if pd.isna(value):
            return None
        
        try:
            # If already a number, return it
            if isinstance(value, (int, float)):
                return float(value)
            
            # Convert to string and clean
            str_value = str(value).strip()
            
            if not str_value or str_value.lower() == 'nan':
                return None
            
            # Handle European formatting (spaces as thousands separator, comma as decimal)
            # Examples: "2 070,00", "1 234,56", "15,00", "405,00"
            
            # Remove currency symbols
            str_value = re.sub(r'[€$£¥₹₽din\s]+', '', str_value, flags=re.IGNORECASE)
            
            # Check if it's European format (comma as decimal separator)
            if ',' in str_value and '.' not in str_value:
                # European format: "2 070,00" or "15,00"
                str_value = str_value.replace(' ', '')  # Remove spaces (thousands separator)
                str_value = str_value.replace(',', '.')  # Convert comma to dot
            elif ',' in str_value and '.' in str_value:
                # Mixed format: determine which is decimal separator
                comma_pos = str_value.rfind(',')
                dot_pos = str_value.rfind('.')
                
                if comma_pos > dot_pos:
                    # Comma is decimal separator: "1.234,56"
                    str_value = str_value.replace('.', '').replace(',', '.')
                else:
                    # Dot is decimal separator: "1,234.56"
                    str_value = str_value.replace(',', '')
            else:
                # Only spaces (thousands separator)
                str_value = str_value.replace(' ', '')
            
            # Final cleanup - keep only digits and one decimal point
            str_value = re.sub(r'[^\d\.]', '', str_value)
            
            if str_value and str_value != '.':
                parsed_value = float(str_value)
                # Sanity check - reject unreasonably large numbers (likely parsing error)
                if parsed_value > 1e12:
                    return None
                return parsed_value
            
            return None
            
        except Exception as e:
            if self.debug:
                print(f"Warning: Could not parse number '{value}': {str(e)}")
            return None
    
    def _categorize_item(self, description: str) -> str:
        """Categorize item based on description keywords"""
        description_lower = description.lower()
        
        # Score each category
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in description_lower:
                    score += len(keyword)  # Longer matches get higher scores
            category_scores[category] = score
        
        # Return category with highest score, or 'ostalo' if no matches
        if category_scores and max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        
        return 'ostalo'  # Default category
    
    def _determine_supplier_type(self, category: str) -> str:
        """Determine what type of supplier is needed for this category"""
        return self.supplier_mapping.get(category, 'Opšti dobavljač')
    
    def _calculate_confidence(self, item: ConstructionItem) -> float:
        """Calculate confidence score for the parsed item"""
        score = 0.0
        
        # Position number confidence
        if item.position_number and item.position_number.isdigit():
            score += 0.2
        
        # Description quality
        if len(item.description) > 10:
            score += 0.3
        
        # Unit presence
        if item.unit:
            score += 0.2
        
        # Quantity validity
        if item.quantity and item.quantity > 0:
            score += 0.2
        
        # Price data
        if item.unit_price and item.unit_price > 0:
            score += 0.1
        
        return min(score, 1.0)
    
    def _create_output_folder(self, input_file_path: str) -> str:
        """Create output folder based on input filename in ./tests/output directory"""
        input_path = Path(input_file_path)
        folder_name = input_path.stem  # filename without extension
        
        # Create the tests/output directory structure
        base_output_dir = Path("tests") / "output"
        output_folder = base_output_dir / folder_name
        
        # Create all necessary directories
        output_folder.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Created output folder: {output_folder}")
        return str(output_folder)
    
    def export_results(self, items: List[ConstructionItem], input_file_path: str, output_path: str = None):
        """Export parsed results to Excel for review"""
        if not items:
            logger.warning("No items to export")
            return
        
        # Create output folder based on input filename
        output_folder = self._create_output_folder(input_file_path)
        
        # Set default output path if not provided
        if output_path is None:
            output_path = Path(output_folder) / "parsed_results.xlsx"
        else:
            output_path = Path(output_folder) / output_path
        
        data = []
        for item in items:
            data.append({
                'Pozicija': item.position_number,
                'Opis': item.description,
                'Jedinica mere': item.unit,
                'Količina': item.quantity,
                'Jedinična cena': item.unit_price,
                'Ukupna cena': item.total_price,
                'Kategorija': item.category,
                'Tip dobavljača': item.supplier_type,
                'Confidence': f"{item.confidence_score:.2f}" if item.confidence_score else "N/A",
                'Kompleksnost': item.complexity,
                'Materijal/Rad': item.material_vs_labor,
                'Rizik': item.risk_level,
                'Tehničke spec.': item.technical_specs
            })
        
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        logger.info(f"Results exported to: {output_path}")
        print(f"📁 Results exported to: {output_path}")
        
        return str(output_path)
    
    def export_json(self, items: List[ConstructionItem], input_file_path: str, output_path: str = None):
        """Export parsed results to JSON"""
        # Create output folder based on input filename
        output_folder = self._create_output_folder(input_file_path)
        
        # Set default output path if not provided
        if output_path is None:
            output_path = Path(output_folder) / "parsed_results.json"
        else:
            output_path = Path(output_folder) / output_path
        
        data = [item.to_dict() for item in items]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"JSON results exported to: {output_path}")
        print(f"📄 JSON results exported to: {output_path}")
        
        return str(output_path)
    
    def export_summary_report(self, items: List[ConstructionItem], input_file_path: str):
        """Export a detailed summary report"""
        output_folder = self._create_output_folder(input_file_path)
        report_path = Path(output_folder) / "summary_report.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("EXCEL PARSER AGENT - SUMMARY REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Input file: {input_file_path}\n")
            f.write(f"Parsed items: {len(items)}\n\n")
            
            # Category breakdown
            categories = {}
            total_value = 0
            items_with_prices = 0
            
            for item in items:
                categories[item.category] = categories.get(item.category, 0) + 1
                if item.total_price:
                    total_value += item.total_price
                    items_with_prices += 1
            
            f.write("CATEGORY BREAKDOWN:\n")
            for category, count in sorted(categories.items()):
                percentage = (count / len(items)) * 100
                f.write(f"  {category}: {count} items ({percentage:.1f}%)\n")
            
            if items_with_prices > 0:
                f.write(f"\nFINANCIAL SUMMARY:\n")
                f.write(f"  Total value: {total_value:,.2f} RSD\n")
                f.write(f"  Items with prices: {items_with_prices}/{len(items)}\n")
                f.write(f"  Average price per item: {total_value/items_with_prices:,.2f} RSD\n")
            
            f.write(f"\nDETAILED ITEMS:\n")
            for i, item in enumerate(items, 1):
                f.write(f"\n{i}. {item.description}\n")
                f.write(f"   Position: {item.position_number} | Quantity: {item.quantity} {item.unit}\n")
                f.write(f"   Category: {item.category} | Supplier: {item.supplier_type}\n")
                if item.unit_price:
                    f.write(f"   Price: {item.unit_price:.2f} RSD/{item.unit}\n")
        
        print(f"📋 Summary report exported to: {report_path}")
        return str(report_path)
    
    def print_summary(self, items: List[ConstructionItem]):
        """Print a comprehensive summary of parsed items"""
        if not items:
            print("❌ No items found in the Excel file")
            return
        
        print(f"\n{'='*50}")
        print(f"📊 ANALIZA EXCEL SPECIFIKACIJE")
        print(f"{'='*50}")
        print(f"📈 Ukupno stavki: {len(items)}")
        
        # Category breakdown
        categories = {}
        total_value = 0
        items_with_prices = 0
        
        for item in items:
            categories[item.category] = categories.get(item.category, 0) + 1
            if item.total_price:
                total_value += item.total_price
                items_with_prices += 1
        
        print(f"\n🏷️  Kategorije:")
        for category, count in sorted(categories.items()):
            percentage = (count / len(items)) * 100
            print(f"  • {category}: {count} stavki ({percentage:.1f}%)")
        
        # Financial summary
        if items_with_prices > 0:
            print(f"\n💰 Finansijski pregled:")
            print(f"  • Ukupna vrednost: {total_value:,.2f} RSD")
            print(f"  • Stavke sa cenama: {items_with_prices}/{len(items)}")
            print(f"  • Prosečna cena po stavci: {total_value/items_with_prices:,.2f} RSD")
        
        # Quality metrics
        avg_confidence = sum(item.confidence_score or 0 for item in items) / len(items)
        print(f"\n📊 Kvalitet parsiranja:")
        print(f"  • Prosečan confidence score: {avg_confidence:.2f}")
        
        high_conf_items = sum(1 for item in items if (item.confidence_score or 0) > 0.8)
        print(f"  • Visok kvalitet (>0.8): {high_conf_items}/{len(items)} stavki")
        
        # Sample items
        print(f"\n📋 Primer stavki:")
        for i, item in enumerate(items[:5]):
            print(f"  {item.position_number}. {item.description[:60]}...")
            print(f"     📦 {item.quantity} {item.unit} | 🏷️ {item.category} | 🏢 {item.supplier_type}")
            if item.unit_price:
                print(f"     💵 {item.unit_price:.2f} RSD/{item.unit}")
        
        if len(items) > 5:
            print(f"     ... i još {len(items) - 5} stavki")
        
        print(f"{'='*50}\n")

def create_test_excel():
    """Create a test Excel file with sample construction data"""
    test_data = {
        'BR.': [1, 2, 3, 4, 5, 6],
        'OPIS POZICIJE': [
            'Izrada otvora za prolaz cevi split klima uređaja kroz AB ploču',
            'Izrada čeličnih hilzni za prolaz bakarnih cevi klima uređaja na krov',
            'Izolacija bakarnih cevi radijatorskog grejanja mineralnom vunom',
            'Montaža ventilacijskih rešetki u fasadi objekta',
            'Probijanje otvora za prolaz elektro instalacija kroz AB ploču',
            'Ugradnja LED rasvete u hodnicima sa prekidačima'
        ],
        'J. MERE': ['kom.', 'kom.', 'm', 'kom.', 'kom.', 'kom.'],
        'KOL.': [27, 5, 150, 8, 12, 15],
        'J. CENA': [15.00, 30.00, 12.30, 125.00, 95.00, 85.00],
        'CENA': [405.00, 150.00, 1845.00, 1000.00, 1140.00, 1275.00]
    }
    
    df = pd.DataFrame(test_data)
    test_file = "test_construction_spec.xlsx"
    df.to_excel(test_file, index=False)
    print(f"✅ Test Excel file created: {test_file}")
    return test_file

def main():
    """Main function to demonstrate the Excel Parser Agent"""
    print("🚀 Excel Parser Agent - Construction Specifications")
    print("🤖 Enhanced with OpenAI LLM Intelligence")
    print("=" * 60)
    
    # Parse command line arguments
    enable_llm = True
    api_key = os.getenv('OPENAI_API_KEY')
    
    # Check for --no-llm flag
    if '--no-llm' in sys.argv:
        enable_llm = False
        sys.argv.remove('--no-llm')
        print("🔄 LLM enhancement disabled")
    
    # Initialize parser
    parser = ExcelParserAgent(
        debug=True, 
        enable_llm=enable_llm,
        openai_api_key=api_key
    )
    
    # Check if user provided a file path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"📁 Using provided file: {file_path}")
        
        # Check if the provided file exists
        if not Path(file_path).exists():
            print(f"❌ Error: File '{file_path}' not found!")
            print("Please check the file path and try again.")
            sys.exit(1)
            
    else:
        # Create test file if no file provided
        print("📝 No file provided, creating test Excel file...")
        file_path = create_test_excel()
    
    try:
        # Parse the Excel file
        items = parser.parse_excel(file_path)
        
        # Print comprehensive summary
        parser.print_summary(items)
        
        # Export results to organized folders
        parser.export_results(items, file_path)
        parser.export_json(items, file_path)
        parser.export_summary_report(items, file_path)
        
        print("✅ Processing completed successfully!")
        print(f"\n📁 All output files saved in: tests/output/{Path(file_path).stem}/ folder")
        print("\n📋 Files created:")
        output_folder = f"tests/output/{Path(file_path).stem}"
        print(f"  📊 {output_folder}/parsed_results.xlsx - Detailed Excel results")
        print(f"  📄 {output_folder}/parsed_results.json - JSON data for APIs")
        print(f"  📋 {output_folder}/summary_report.txt - Text summary report")
        
        if enable_llm:
            print(f"\n🤖 LLM Enhancement Features:")
            print(f"  • Advanced categorization with GPT-4")
            print(f"  • Complexity analysis (1-5 scale)")
            print(f"  • Material vs Labor classification")
            print(f"  • Risk assessment")
            print(f"  • Technical specification extraction")
        
        print("\n🚀 Next steps:")
        print("  1. Review the Excel file for detailed results")
        print("  2. Use JSON data for the next agent (Supplier Mapping)")
        print("  3. Check summary report for quick overview")
        
        if not enable_llm and not api_key:
            print(f"\n💡 Tip: Set OPENAI_API_KEY environment variable for LLM enhancement")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        logger.error(f"Main execution failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()