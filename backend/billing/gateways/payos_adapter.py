import hashlib
import hmac
import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any

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

    def _post_json(self, url: str, payload: dict, headers: dict, timeout: int = 10) -> dict:
        """Send a POST request with JSON body using urllib (stdlib).

        Uses ``urllib.request`` instead of the pip ``requests`` library
        because the legacy Django app ``backend/requests/`` shadows it.
        """
        # Ensure User-Agent is set to avoid Cloudflare 403/1010 blocks
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'RentEase/1.0'
        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            # Try to parse error body
            try:
                body = json.loads(e.read().decode('utf-8'))
            except Exception:
                body = {"code": str(e.code), "desc": f"HTTP Error {e.code}: {e.reason}"}
            return body
        except urllib.error.URLError as e:
            raise PayOSGatewayError(f"PayOS network error: {str(e)}")

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
            response_data = self._post_json(endpoint, payload, headers, timeout=10)
            
            if response_data.get('code') != '00':
                raise PayOSGatewayError(f"PayOS API Error: {response_data.get('desc')}")
                
            return response_data.get('data', {})
        except PayOSGatewayError:
            raise
        except Exception as e:
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
            response_data = self._post_json(endpoint, payload, headers, timeout=10)
            return response_data.get('code') == '00'
        except Exception:
            return False

    def _get_json(self, url: str, headers: dict, timeout: int = 10) -> dict:
        """Send a GET request expecting JSON."""
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'RentEase/1.0'
        if 'Accept' not in headers:
            headers['Accept'] = 'application/json'

        req = urllib.request.Request(url, headers=headers, method='GET')
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read().decode('utf-8'))
            except Exception:
                body = {"code": str(e.code), "desc": f"HTTP Error {e.code}: {e.reason}"}
            return body
        except urllib.error.URLError as e:
            raise PayOSGatewayError(f"PayOS network error: {str(e)}")

    def get_payment_link_info(self, order_code: int) -> Dict:
        """Get payment link information by order_code."""
        endpoint = f"{self.BASE_URL}/v2/payment-requests/{order_code}"
        
        headers = {
            "x-client-id": self.client_id,
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        
        try:
            response_data = self._get_json(endpoint, headers, timeout=10)
            
            if response_data.get('code') != '00':
                raise PayOSGatewayError(f"PayOS API Error: {response_data.get('desc')}")
                
            return response_data.get('data', {})
        except PayOSGatewayError:
            raise
        except Exception as e:
            logger.error(f"PayOS Request Failed: {e}")
            raise PayOSGatewayError(f"PayOS network error: {str(e)}")
