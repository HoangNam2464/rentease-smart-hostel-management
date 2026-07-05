from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import PrivateDocument, AuditEvent

User = get_user_model()

class GovernanceModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin_test', password='password123')
        # We need a dummy object to attach GenericForeignKey to. User model is fine.
        self.content_type = ContentType.objects.get_for_model(User)
        
    def test_create_private_document(self):
        doc = PrivateDocument.objects.create(
            category=PrivateDocument.CATEGORY_IDENTITY,
            owner=self.user,
            content_type=self.content_type,
            object_id=self.user.id,
            storage_key='private/identities/admin_test_id.jpg'
        )
        self.assertEqual(doc.category, PrivateDocument.CATEGORY_IDENTITY)
        self.assertEqual(doc.retention_status, PrivateDocument.STATUS_ACTIVE)
        self.assertEqual(doc.subject, self.user)
        self.assertIsNotNone(doc.created_at)
        
    def test_create_audit_event(self):
        event = AuditEvent.objects.create(
            actor=self.user,
            action='view_identity',
            content_type=self.content_type,
            object_id=self.user.id,
            ip_address='127.0.0.1',
            details={'reason': 'verification'}
        )
        self.assertEqual(event.action, 'view_identity')
        self.assertEqual(event.actor, self.user)
        self.assertEqual(event.target, self.user)
        self.assertEqual(event.ip_address, '127.0.0.1')
        self.assertEqual(event.details['reason'], 'verification')
