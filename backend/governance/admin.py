from django.contrib import admin
from .models import PrivateDocument, AuditEvent

@admin.register(PrivateDocument)
class PrivateDocumentAdmin(admin.ModelAdmin):
    list_display = ['category', 'owner', 'content_type', 'object_id', 'retention_status', 'created_at']
    list_filter = ['category', 'retention_status', 'created_at']
    search_fields = ['owner__username', 'storage_key']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ['action', 'actor', 'content_type', 'object_id', 'ip_address', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['actor__username', 'action', 'ip_address']
    
    # AuditEvent should be mostly read-only to preserve audit trail
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
