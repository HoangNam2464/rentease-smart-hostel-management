from django.urls import path
from billing.api.webhooks import PayOSWebhookAPIView

app_name = 'billing_api'

urlpatterns = [
    path('webhooks/payos/', PayOSWebhookAPIView.as_view(), name='payos_webhook'),
]
