#!/usr/bin/env python3
"""
Communication Agent for Construction Industry
Sends requests to suppliers via email and API calls
"""

import smtplib
import logging
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
import time

logger = logging.getLogger(__name__)

@dataclass
class CommunicationRequest:
    """Request to be sent to supplier"""
    supplier_name: str
    supplier_email: str
    items: List[Dict]
    request_id: str
    message_template: str = "standard"

@dataclass
class CommunicationResult:
    """Result of communication attempt"""
    request_id: str
    supplier_name: str
    success: bool
    method: str  # email, api, etc.
    timestamp: str
    error_message: Optional[str] = None

class CommunicationAgent:
    """Handles communication with suppliers"""
    
    def __init__(self, smtp_server: str = None, smtp_port: int = 587):
        self.smtp_server = smtp_server or "smtp.gmail.com"
        self.smtp_port = smtp_port
        self.email_templates = self._load_email_templates()
        
    def _load_email_templates(self) -> Dict[str, str]:
        """Load email templates"""
        return {
            "standard": """
Poštovani,

Molimo Vas da nam dostavite ponudu za sledeće pozicije:

{items_list}

Molimo da odgovorite sa cenama u najkraćem mogućem roku.

Hvala vam,
Konstrukcijski tim
""",
            "urgent": """
HITNO - Ponuda potrebna

Poštovani,

Hitno potrebna ponuda za:
{items_list}

Odgovorite u roku od 2 sata.

Hvala,
Konstrukcijski tim
"""
        }
    
    def send_requests(self, requests: List[CommunicationRequest]) -> List[CommunicationResult]:
        """Send requests to all suppliers"""
        logger.info(f"Sending {len(requests)} requests to suppliers...")
        
        results = []
        
        for request in requests:
            result = self._send_single_request(request)
            results.append(result)
            
            # Rate limiting
            time.sleep(1)
        
        success_count = sum(1 for r in results if r.success)
        logger.info(f"Successfully sent {success_count}/{len(results)} requests")
        
        return results
    
    def _send_single_request(self, request: CommunicationRequest) -> CommunicationResult:
        """Send request to a single supplier"""
        try:
            # For demo purposes, we'll just log the email instead of actually sending
            items_text = self._format_items_for_email(request.items)
            template = self.email_templates.get(request.message_template, self.email_templates["standard"])
            message = template.format(items_list=items_text)
            
            logger.info(f"📧 [DEMO] Sending email to {request.supplier_name} ({request.supplier_email})")
            logger.info(f"Subject: Zahtev za ponudu - {request.request_id}")
            logger.info(f"Message preview: {message[:100]}...")
            
            # In real implementation, would use SMTP here
            # self._send_email(request.supplier_email, subject, message)
            
            return CommunicationResult(
                request_id=request.request_id,
                supplier_name=request.supplier_name,
                success=True,
                method="email",
                timestamp=str(time.time())
            )
            
        except Exception as e:
            logger.error(f"Failed to send request to {request.supplier_name}: {str(e)}")
            return CommunicationResult(
                request_id=request.request_id,
                supplier_name=request.supplier_name,
                success=False,
                method="email",
                timestamp=str(time.time()),
                error_message=str(e)
            )
    
    def _format_items_for_email(self, items: List[Dict]) -> str:
        """Format items list for email"""
        lines = []
        for i, item in enumerate(items, 1):
            lines.append(f"{i}. {item.get('description', 'N/A')}")
            lines.append(f"   Količina: {item.get('quantity', 0)} {item.get('unit', '')}")
            lines.append("")
        
        return "\n".join(lines)
    
    def export_communication_log(self, results: List[CommunicationResult], output_path: str):
        """Export communication results to JSON"""
        export_data = [
            {
                'request_id': r.request_id,
                'supplier_name': r.supplier_name,
                'success': r.success,
                'method': r.method,
                'timestamp': r.timestamp,
                'error_message': r.error_message
            }
            for r in results
        ]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Communication log exported to: {output_path}")

def main():
    """Test the Communication Agent"""
    print("📤 Communication Agent Test")
    
    # Demo requests
    demo_requests = [
        CommunicationRequest(
            supplier_name="HVAC Sistem doo",
            supplier_email="office@hvacsistem.rs",
            items=[{'description': 'Split klima uređaj', 'quantity': 5, 'unit': 'kom'}],
            request_id="REQ001"
        ),
        CommunicationRequest(
            supplier_name="Elektro Montaža",
            supplier_email="info@elektromontaza.rs",
            items=[{'description': 'LED rasveta', 'quantity': 10, 'unit': 'kom'}],
            request_id="REQ002"
        )
    ]
    
    agent = CommunicationAgent()
    results = agent.send_requests(demo_requests)
    
    print("\nResults:")
    for result in results:
        status = "✅" if result.success else "❌"
        print(f"  {status} {result.supplier_name}: {result.method}")

if __name__ == "__main__":
    main()
