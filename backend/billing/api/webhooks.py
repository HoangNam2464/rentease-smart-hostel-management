import logging
from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from billing.gateways.payos_adapter import PayOSGateway
from billing.models import PaymentIntent, PaymentHistory, PaymentWebhookEvent

logger = logging.getLogger(__name__)

class PayOSWebhookAPIView(APIView):
    """
    Receives and processes webhooks from PayOS.
    """
    authentication_classes = []  # No token needed, verified via HMAC signature
    permission_classes = []
    
    def post(self, request, *args, **kwargs):
        payload = request.data
        
        # Structure from PayOS webhook
        if not payload or not isinstance(payload, dict):
            return Response({"error": "Invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
            
        code = payload.get('code')
        if code != '00':
            logger.warning(f"PayOS Webhook error code: {code}, payload: {payload}")
            # Still acknowledge to prevent resending
            return Response({"message": "Acknowledged"}, status=status.HTTP_200_OK)
            
        data = payload.get('data', {})
        if not data:
            return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)
            
        order_code = data.get('orderCode')
        if not order_code:
            return Response({"error": "Missing orderCode"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Verify Signature
        gateway = PayOSGateway()
        if not gateway.verify_webhook_signature(payload):
            logger.error(f"PayOS Webhook invalid signature. payload: {payload}")
            return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

        event_name = data.get('desc', 'payos_transfer')
        
        with transaction.atomic():
            # Idempotency check: has this specific webhook event been processed?
            # We use order_code and maybe the reference to ensure we don't process same webhook.
            # But the webhook itself might be repeated. 
            # We record every webhook.
            webhook_event = PaymentWebhookEvent.objects.create(
                provider='payos',
                order_code=str(order_code),
                event_name=event_name,
                payload=payload,
                is_processed=False
            )
            
            try:
                # Lock the intent to avoid race conditions
                intent = PaymentIntent.objects.select_for_update().get(order_code=str(order_code))
            except PaymentIntent.DoesNotExist:
                logger.error(f"PaymentIntent with order_code {order_code} not found.")
                # We save it but return 200 so PayOS stops sending
                return Response({"message": "Intent not found"}, status=status.HTTP_200_OK)

            if intent.status in [PaymentIntent.STATUS_PAID, PaymentIntent.STATUS_CANCELLED]:
                # Already processed
                webhook_event.is_processed = True
                webhook_event.save()
                return Response({"message": "Already processed"}, status=status.HTTP_200_OK)

            # Check amount
            received_amount = Decimal(str(data.get('amount', 0)))
            expected_amount = intent.amount

            if received_amount >= expected_amount:
                # Paid in full or overpaid
                # For MVP, if it's overpaid we still mark it paid, maybe owner checks later, 
                # but let's stick to user instructions: "Nếu sai số tiền -> review".
                # User says: "Sai số tiền -> chuyển sang review".
                if received_amount == expected_amount:
                    intent.status = PaymentIntent.STATUS_PAID
                    intent.save()

                    # Create PaymentHistory
                    history = PaymentHistory.objects.create(
                        invoice=intent.invoice,
                        amount=received_amount,
                        method=PaymentHistory.METHOD_BANK_TRANSFER,
                        transaction_code=str(data.get('reference', '')),
                        paid_at=timezone.now(),
                        note=f"PayOS auto-payment (Ref: {data.get('reference')})"
                    )
                    
                    intent.payment_history = history
                    intent.save()
                else:
                    intent.status = PaymentIntent.STATUS_REVIEW
                    intent.save()
                    logger.warning(f"Payment amount mismatch for order {order_code}. Expected {expected_amount}, got {received_amount}")
            else:
                # Underpaid
                intent.status = PaymentIntent.STATUS_REVIEW
                intent.save()
                logger.warning(f"Payment underpaid for order {order_code}. Expected {expected_amount}, got {received_amount}")

            webhook_event.is_processed = True
            webhook_event.save()

        return Response({"success": True, "message": "Webhook processed"}, status=status.HTTP_200_OK)
