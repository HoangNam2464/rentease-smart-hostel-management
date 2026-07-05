import hashlib
import hmac
import json
import logging
from typing import Dict, Any

import requests
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

class PayOSGatewayError(Exception):
    pass

class PayOSGateway:
    """Adapter for PayOS API."""
    
    BASE_URL = "https://api-merchant.payos.vn"

    def __init__(self):
        self.client_id = getattr(settings, 'PAYOS_CLIENT_ID', '')
        self.api_key = getattr(settings, 'PAYOS_API_KEY', '')
        self.checksum_key = getattr(settings, 'PAYOS_CHECKSUM_KEY', '')

        if not all([self.client_id, self.api_key, self.checksum_key]):
            logger.warning("PayOS credentials are not fully configured in settings.")

    def _generate_signature(self, data: Dict[str, Any]) -> str:
        """Generate HMAC-SHA256 signature for PayOS request."""
        # Sort keys alphabetically and filter out None or empty values if necessary
        # According to PayOS docs, signature is created from sorted specific keys
        sign_data = {
            "amount": data.get("amount"),
            "cancelUrl": data.get("cancelUrl"),
            "description": data.get("description"),
            "orderCode": data.get("orderCode"),
            "returnUrl": data.get("returnUrl")
        }
        
        # Filter out None values
        sign_data = {k: v for k, v in sign_data.items() if v is not None}
        
        # Sort by key and create query string
        sorted_keys = sorted(sign_data.keys())
        query_string = "&".join([f"{k}={sign_data[k]}" for k in sorted_keys])
        
        signature = hmac.new(
            self.checksum_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return signature

    def create_payment_link(self, order_code: int, amount: int, description: str, return_url: str, cancel_url: str) -> Dict:
        """
        Creates a payment link via PayOS.
        order_code must be an integer (up to 53-bit).
        amount must be an integer.
        """
        endpoint = f"{self.BASE_URL}/v2/payment-requests"
        
        payload = {
            "orderCode": order_code,
            "amount": amount,
            "description": description[:25], # PayOS limit
            "returnUrl": return_url,
            "cancelUrl": cancel_url
        }
        
        payload["signature"] = self._generate_signature(payload)
        
        headers = {
            "x-client-id": self.client_id,
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
            response_data = response.json()
            
            if response_data.get('code') != '00':
                raise PayOSGatewayError(f"PayOS API Error: {response_data.get('desc')}")
                
            return response_data.get('data', {})
        except requests.exceptions.RequestException as e:
            logger.error(f"PayOS Request Failed: {e}")
            raise PayOSGatewayError(f"PayOS network error: {str(e)}")

    def verify_webhook_signature(self, payload: Dict[str, Any]) -> bool:
        """
        Verify the signature of incoming PayOS webhook.
        payload is the JSON dictionary received.
        """
        data = payload.get('data', {})
        signature = payload.get('signature', '')
        
        # For webhook verification, data string format is:
        # amount=...&amount_not_pay=...&code=...&counterAccountBankId=...
        # PayOS Webhook data format has its own set of keys
        
        # Exclude 'signature' from data to sort
        sign_data = {k: v for k, v in data.items() if k != 'signature'}
        
        # Sort and build query string
        sorted_keys = sorted(sign_data.keys())
        # Convert values to string, handling None
        parts = []
        for k in sorted_keys:
            v = sign_data[k]
            if v is None:
                parts.append(f"{k}=")
            elif isinstance(v, (list, dict)):
                parts.append(f"{k}={json.dumps(v, separators=(',', ':'))}")
            else:
                parts.append(f"{k}={v}")
                
        query_string = "&".join(parts)
        
        expected_signature = hmac.new(
            self.checksum_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return expected_signature == signature

    def cancel_payment_link(self, order_code: int, cancellation_reason: str = "") -> bool:
        """Cancels an existing payment link."""
        endpoint = f"{self.BASE_URL}/v2/payment-requests/{order_code}/cancel"
        
        payload = {
            "cancellationReason": cancellation_reason[:250]
        }
        
        headers = {
            "x-client-id": self.client_id,
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
            response_data = response.json()
            return response_data.get('code') == '00'
        except requests.exceptions.RequestException:
            return False
