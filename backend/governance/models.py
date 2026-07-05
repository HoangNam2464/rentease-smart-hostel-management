from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class PrivateDocument(models.Model):
    CATEGORY_IDENTITY = 'identity_card'
    CATEGORY_CONTRACT = 'contract'
    CATEGORY_EVIDENCE = 'maintenance_evidence'

    CATEGORY_CHOICES = (
        (CATEGORY_IDENTITY, 'Identity Card / Passport'),
        (CATEGORY_CONTRACT, 'Signed Contract'),
        (CATEGORY_EVIDENCE, 'Maintenance Evidence'),
    )

    STATUS_ACTIVE = 'active'
    STATUS_ARCHIVED = 'archived'
    STATUS_DELETION = 'marked_for_deletion'

    STATUS_CHOICES = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_ARCHIVED, 'Archived'),
        (STATUS_DELETION, 'Marked for Deletion'),
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='private_documents')
    
    # Generic relation to Tenant, Contract, MaintenanceRecord, etc.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    subject = GenericForeignKey('content_type', 'object_id')

    storage_key = models.CharField(max_length=512, help_text="Path or UUID to the private storage object")
    retention_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gov_private_document'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['category']),
            models.Index(fields=['retention_status']),
        ]

    def __str__(self):
        return f"{self.get_category_display()} - {self.storage_key}"

class AuditEvent(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_events')
    action = models.CharField(max_length=100)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'gov_audit_event'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['action']),
            models.Index(fields=['actor']),
        ]

    def __str__(self):
        return f"{self.actor} performed {self.action} on {self.content_type} ({self.object_id})"
