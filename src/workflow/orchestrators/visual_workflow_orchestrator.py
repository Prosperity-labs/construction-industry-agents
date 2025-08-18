#!/usr/bin/env python3
"""
Visual Workflow Monitor for Construction Industry Agents
Shows real-time progress with visual indicators and step-by-step breakdown
"""

import time
import sys
import json
import os
from pathlib import Path
from typing import Dict, List, Optional
import threading
from datetime import datetime

# Import all the agents
from src.domains.parsing.agents.excel_parser_agent import ExcelParserAgent
from src.domains.suppliers.agents.supplier_mapping_agent import SupplierMappingAgent
from src.domains.communication.agents.communication_agent import CommunicationAgent, CommunicationRequest
from src.domains.responses.agents.response_parser_agent import ResponseParserAgent
from src.domains.quotes.agents.quote_calculator_agent import QuoteCalculatorAgent
from src.domains.documents.agents.document_generator_agent import DocumentGeneratorAgent

class VisualWorkflowMonitor:
    """Visual monitor for the construction workflow with real-time updates"""
    
    def __init__(self, enable_llm: bool = False):
        self.enable_llm = enable_llm
        self.workflow_id = f"VISUAL_{int(time.time())}"
        self.steps = [
            {"name": "📊 Excel Parsing", "status": "pending", "details": "", "duration": 0},
            {"name": "🏭 Supplier Mapping", "status": "pending", "details": "", "duration": 0},
            {"name": "📤 Communication", "status": "pending", "details": "", "duration": 0},
            {"name": "📥 Response Processing", "status": "pending", "details": "", "duration": 0},
            {"name": "🧮 Quote Calculation", "status": "pending", "details": "", "duration": 0},
            {"name": "📄 Document Generation", "status": "pending", "details": "", "duration": 0}
        ]
        self.current_step = 0
        self.start_time = time.time()
        
        # Initialize agents
        self.excel_parser = ExcelParserAgent(debug=False, enable_llm=enable_llm)
        self.supplier_mapper = SupplierMappingAgent()
        self.communicator = CommunicationAgent()
        self.response_parser = ResponseParserAgent()
        self.quote_calculator = QuoteCalculatorAgent()
        self.document_generator = DocumentGeneratorAgent()
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        """Print the workflow header"""
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "🏗️  CONSTRUCTION WORKFLOW MONITOR" + " " * 21 + "║")
        print("╠" + "═" * 78 + "╣")
        print(f"║ Workflow ID: {self.workflow_id:<25} │ Started: {datetime.now().strftime('%H:%M:%S'):<15} ║")
        print(f"║ Status: {'🟢 RUNNING':<32} │ Elapsed: {time.time() - self.start_time:>6.1f}s" + " " * 8 + "║")
        print("╚" + "═" * 78 + "╝")
    
    def print_workflow_diagram(self):
        """Print a visual workflow diagram"""
        print("\n📋 WORKFLOW OVERVIEW:")
        print("┌─────────────────────────────────────────────────────────────────────────┐")
        print("│  📊 Excel → 🏭 Suppliers → 📤 Requests → 📥 Responses → 🧮 Quote → 📄 Docs │")
        print("└─────────────────────────────────────────────────────────────────────────┘")
    
    def print_step_status(self):
        """Print current step status with visual indicators"""
        print(f"\n⏱️  STEP PROGRESS:")
        
        for i, step in enumerate(self.steps):
            # Status indicators
            if step["status"] == "completed":
                status_icon = "✅"
                status_text = "COMPLETED"
            elif step["status"] == "running":
                status_icon = "🔄"
                status_text = "RUNNING"
            elif step["status"] == "pending":
                status_icon = "⏳"
                status_text = "PENDING"
            else:
                status_icon = "❌"
                status_text = "FAILED"
            
            # Duration display
            duration_text = f"{step['duration']:.1f}s" if step['duration'] > 0 else ""
            
            # Current step highlight
            if i == self.current_step and step["status"] == "running":
                print(f"  ➤ {status_icon} {step['name']:<25} │ {status_text:<10} │ {duration_text:>6}")
            else:
                print(f"    {status_icon} {step['name']:<25} │ {status_text:<10} │ {duration_text:>6}")
            
            # Show details for completed or running steps
            if step["details"] and (step["status"] in ["completed", "running"]):
                print(f"      └─ {step['details']}")
    
    def print_live_data(self, data: Dict = None):
        """Print live data during processing"""
        if not data:
            return
            
        print(f"\n📊 LIVE DATA:")
        print("┌─────────────────────────────────────────────────────────────────────────┐")
        
        for key, value in data.items():
            print(f"│ {key:<25}: {str(value):<45} │")
        
        print("└─────────────────────────────────────────────────────────────────────────┘")
    
    def print_progress_bar(self, current: int, total: int, step_name: str = ""):
        """Print a progress bar for the current operation"""
        if total == 0:
            return
            
        percentage = (current / total) * 100
        bar_length = 50
        filled_length = int(bar_length * current // total)
        
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        print(f"\n🔄 {step_name}: [{bar}] {percentage:.1f}% ({current}/{total})")
    
    def update_step(self, step_index: int, status: str, details: str = "", duration: float = 0):
        """Update step status and refresh display"""
        if 0 <= step_index < len(self.steps):
            self.steps[step_index]["status"] = status
            self.steps[step_index]["details"] = details
            self.steps[step_index]["duration"] = duration
            self.current_step = step_index
        
        self.refresh_display()
    
    def refresh_display(self, live_data: Dict = None):
        """Refresh the entire display"""
        self.clear_screen()
        self.print_header()
        self.print_workflow_diagram()
        self.print_step_status()
        
        if live_data:
            self.print_live_data(live_data)
        
        # Add a small delay to make updates visible
        time.sleep(0.5)
    
    def run_visual_workflow(self, excel_file_path: str) -> Dict:
        """Run the complete workflow with visual monitoring"""
        self.refresh_display()
        
        try:
            output_folder = Path("visual_workflow_output")
            output_folder.mkdir(parents=True, exist_ok=True)
            
            # Step 1: Excel Parsing
            self.update_step(0, "running", "Loading Excel file...")
            step_start = time.time()
            
            parsed_items = self.excel_parser.parse_excel(excel_file_path)
            items_data = [item.to_dict() for item in parsed_items]
            
            step_duration = time.time() - step_start
            self.update_step(0, "completed", f"Parsed {len(parsed_items)} items", step_duration)
            
            self.refresh_display({
                "Excel File": Path(excel_file_path).name,
                "Items Found": len(parsed_items),
                "Categories": len(set(item.get('category', 'unknown') for item in items_data))
            })
            
            # Step 2: Supplier Mapping
            self.update_step(1, "running", "Finding suppliers for each category...")
            step_start = time.time()
            
            supplier_mappings = self.supplier_mapper.map_suppliers(items_data)
            
            step_duration = time.time() - step_start
            self.update_step(1, "completed", f"Mapped {len(supplier_mappings)} items to suppliers", step_duration)
            
            # Count unique suppliers
            unique_suppliers = set()
            for mappings in supplier_mappings.values():
                for match in mappings:
                    unique_suppliers.add(match.supplier.name)
            
            self.refresh_display({
                "Items Mapped": len(supplier_mappings),
                "Unique Suppliers": len(unique_suppliers),
                "Top Supplier": list(unique_suppliers)[0] if unique_suppliers else "None"
            })
            
            # Step 3: Communication
            self.update_step(2, "running", "Sending requests to suppliers...")
            step_start = time.time()
            
            communication_requests = self._create_communication_requests(items_data, supplier_mappings)
            
            # Show progress as requests are sent
            for i, request in enumerate(communication_requests):
                self.print_progress_bar(i + 1, len(communication_requests), "Sending Requests")
                time.sleep(1)  # Simulate sending time
            
            communication_results = self.communicator.send_requests(communication_requests)
            
            step_duration = time.time() - step_start
            successful_requests = sum(1 for r in communication_results if r.success)
            self.update_step(2, "completed", f"Sent {successful_requests}/{len(communication_requests)} requests", step_duration)
            
            self.refresh_display({
                "Requests Sent": len(communication_requests),
                "Successful": successful_requests,
                "Response Time": "15-25 minutes (simulated)"
            })
            
            # Step 4: Response Processing
            self.update_step(3, "running", "Processing supplier responses...")
            step_start = time.time()
            
            # Create demo responses
            demo_responses = self._create_demo_responses(items_data, supplier_mappings)
            
            step_duration = time.time() - step_start
            self.update_step(3, "completed", f"Processed {len(demo_responses)} responses", step_duration)
            
            total_offers = sum(len(r.get('items', [])) for r in demo_responses)
            self.refresh_display({
                "Responses Received": len(demo_responses),
                "Total Price Offers": total_offers,
                "Best Prices": "Automatically selected"
            })
            
            # Step 5: Quote Calculation
            self.update_step(4, "running", "Calculating optimal quote...")
            step_start = time.time()
            
            quote_calculation = self.quote_calculator.calculate_quote(
                items_data, demo_responses, f"QUOTE_{self.workflow_id}"
            )
            
            step_duration = time.time() - step_start
            self.update_step(4, "completed", f"Quote: {quote_calculation.final_total:,.2f} RSD", step_duration)
            
            self.refresh_display({
                "Quote Items": len(quote_calculation.items),
                "Subtotal": f"{quote_calculation.subtotal:,.2f} RSD",
                "Final Total": f"{quote_calculation.final_total:,.2f} RSD",
                "Suppliers Used": len(quote_calculation.supplier_breakdown)
            })
            
            # Step 6: Document Generation
            self.update_step(5, "running", "Generating professional documents...")
            step_start = time.time()
            
            quote_data = {
                'quote_id': quote_calculation.quote_id,
                'calculation_timestamp': quote_calculation.calculation_timestamp,
                'summary': {
                    'subtotal': quote_calculation.subtotal,
                    'margin_total': quote_calculation.margin_total,
                    'tax_total': quote_calculation.tax_total,
                    'final_total': quote_calculation.final_total
                },
                'supplier_breakdown': quote_calculation.supplier_breakdown,
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
                    for item in quote_calculation.items
                ]
            }
            
            generated_files = self.document_generator.generate_documents(quote_data, str(output_folder))
            
            step_duration = time.time() - step_start
            self.update_step(5, "completed", f"Generated {len(generated_files)} documents", step_duration)
            
            # Final display
            total_time = time.time() - self.start_time
            self.refresh_display({
                "Documents Created": len(generated_files),
                "Output Folder": str(output_folder),
                "Total Time": f"{total_time:.1f} seconds",
                "Status": "✅ COMPLETED SUCCESSFULLY!"
            })
            
            # Show final summary
            self.print_final_summary(quote_calculation, generated_files, total_time)
            
            return {
                "success": True,
                "workflow_id": self.workflow_id,
                "total_time": total_time,
                "quote_total": quote_calculation.final_total,
                "files_generated": generated_files
            }
            
        except Exception as e:
            self.update_step(self.current_step, "failed", f"Error: {str(e)}")
            print(f"\n❌ WORKFLOW FAILED: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def print_final_summary(self, quote_calculation, generated_files, total_time):
        """Print the final workflow summary"""
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 25 + "🎉 WORKFLOW COMPLETED!" + " " * 26 + "║")
        print("╠" + "═" * 78 + "╣")
        print(f"║ Total Time: {total_time:.1f}s" + " " * 20 + f"Quote Total: {quote_calculation.final_total:>12,.2f} RSD ║")
        print(f"║ Items Processed: {len(quote_calculation.items):<10}" + " " * 15 + f"Files Generated: {len(generated_files):>12} ║")
        print("╠" + "═" * 78 + "╣")
        print("║ Generated Files:" + " " * 60 + "║")
        
        for file_path in generated_files:
            filename = Path(file_path).name
            print(f"║   📄 {filename:<70} ║")
        
        print("╚" + "═" * 78 + "╝")
        
        print(f"\n💡 RESULT: Quote generated in {total_time:.1f} seconds instead of 2-5 days!")
        print(f"🎯 Time Savings: {((5*24*3600 - total_time) / (5*24*3600)) * 100:.1f}% faster than manual process")
    
    def _create_communication_requests(self, items: List[Dict], mappings: Dict) -> List[CommunicationRequest]:
        """Create communication requests for suppliers"""
        requests = []
        supplier_items = {}
        
        # Group items by supplier
        for item in items:
            position = item.get('position_number', 'unknown')
            if position in mappings:
                matches = mappings[position]
                if matches:
                    best_match = matches[0]
                    supplier = best_match.supplier
                    
                    if supplier.name not in supplier_items:
                        supplier_items[supplier.name] = {
                            'supplier': supplier,
                            'items': []
                        }
                    
                    supplier_items[supplier.name]['items'].append(item)
        
        # Create requests for each supplier
        for supplier_name, data in supplier_items.items():
            request = CommunicationRequest(
                supplier_name=supplier_name,
                supplier_email=data['supplier'].contact_email,
                items=data['items'],
                request_id=f"REQ_{self.workflow_id}_{supplier_name.replace(' ', '_')}"
            )
            requests.append(request)
        
        return requests
    
    def _create_demo_responses(self, items: List[Dict], mappings: Dict) -> List[Dict]:
        """Create demo supplier responses"""
        responses = []
        suppliers = ['HVAC Sistem doo', 'Elektro Montaža', 'Izolacija Plus']
        
        for i, supplier in enumerate(suppliers):
            response_items = []
            
            for item in items[:2]:  # Each supplier responds to first 2 items
                base_price = item.get('unit_price', 100)
                price_factor = 0.9 + (i * 0.1)  # 0.9, 1.0, 1.1
                
                response_items.append({
                    'position': item.get('position_number'),
                    'description': item.get('description'),
                    'unit_price': base_price * price_factor,
                    'quantity': item.get('quantity', 1),
                    'total_price': base_price * price_factor * item.get('quantity', 1),
                    'unit': item.get('unit'),
                    'confidence': 0.9
                })
            
            responses.append({
                'supplier_name': supplier,
                'request_id': f"REQ_{self.workflow_id}_{supplier.replace(' ', '_')}",
                'response_type': 'email',
                'items': response_items
            })
        
        return responses

def main():
    """Main function for visual workflow monitoring"""
    print("🏗️ Construction Industry Visual Workflow Monitor")
    print("=" * 60)
    
    # Check for command line arguments
    enable_llm = '--enable-llm' in sys.argv
    excel_file = None
    
    # Look for Excel file argument
    for arg in sys.argv[1:]:
        if arg.endswith('.xlsx') or arg.endswith('.xls'):
            excel_file = arg
            break
    
    if not excel_file or not Path(excel_file).exists():
        print("📝 No valid Excel file provided, using test file...")
        excel_file = "test_construction_spec.xlsx"
        
        # Create test file if it doesn't exist
        if not Path(excel_file).exists():
            print("📝 Creating test Excel file...")
            from src.domains.parsing.agents.excel_parser_agent import create_test_excel
            excel_file = create_test_excel()
    
    print(f"📁 Input file: {excel_file}")
    print("🔄 Starting visual workflow in 3 seconds...")
    time.sleep(3)
    
    # Initialize and run visual monitor
    monitor = VisualWorkflowMonitor(enable_llm=enable_llm)
    result = monitor.run_visual_workflow(excel_file)
    
    if result["success"]:
        print(f"\n✅ Visual workflow completed successfully!")
        print(f"📁 Check output: visual_workflow_output/")
    else:
        print(f"\n❌ Visual workflow failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()