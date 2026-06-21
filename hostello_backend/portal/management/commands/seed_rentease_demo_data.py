from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts.models import UserProfile
from billing.models import Invoice, InvoiceDetail, PaymentHistory, PriceConfig
from contracts.models import Contract
from listings.models import RoomListing, ViewingRegistration
from maintenance.models import Notification, RepairRequest
from properties.models import Room
from tenants.models import Tenant


DEMO_PREFIX = "DEMO-"
DEMO_EMAIL_DOMAIN = "@example.test"


class Command(BaseCommand):
    help = "Seed safe local-only RentEase demo data for owner/tenant portal walkthroughs."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show intended changes without writing data.")
        parser.add_argument(
            "--reset-demo-data",
            action="store_true",
            help="Delete command-created demo-prefixed data before seeding.",
        )
        parser.add_argument("--owner-username", default="owner_test")
        parser.add_argument("--tenant-username", default="tenant_test")

    def handle(self, *args, **options):
        self.dry_run = options["dry_run"]
        self.reset_demo_data = options["reset_demo_data"]
        self.owner_username = options["owner_username"]
        self.tenant_username = options["tenant_username"]
        self.actions = []

        self._guard_local_only()
        owner_user, owner_profile, tenant_user, tenant = self._load_required_accounts()

        if self.dry_run:
            self._print_dry_run(owner_user, owner_profile, tenant_user, tenant)
            return

        with transaction.atomic():
            if self.reset_demo_data:
                self._reset_demo_data(owner_profile, tenant)
            self._seed(owner_user, owner_profile, tenant_user, tenant)

        self.stdout.write(self.style.SUCCESS("RentEase demo data seed completed."))
        for action in self.actions:
            self.stdout.write(f"- {action}")

    def _guard_local_only(self):
        if not settings.DEBUG:
            raise CommandError("Refusing to seed demo data unless DEBUG=True.")
        self._guard_demo_username(self.owner_username, "owner username")
        self._guard_demo_username(self.tenant_username, "tenant username")

    def _guard_demo_username(self, username, label):
        if username in {"owner_test", "tenant_test", "admin_test"}:
            return
        if username.startswith("demo_") or username.endswith("_test"):
            return
        raise CommandError(
            f"Unsafe {label} '{username}'. Use a local demo/test account such as owner_test or tenant_test."
        )

    def _load_required_accounts(self):
        User = get_user_model()
        try:
            owner_user = User.objects.get(username=self.owner_username)
        except User.DoesNotExist as exc:
            raise CommandError(f"Owner user '{self.owner_username}' does not exist.") from exc

        try:
            tenant_user = User.objects.get(username=self.tenant_username)
        except User.DoesNotExist as exc:
            raise CommandError(f"Tenant user '{self.tenant_username}' does not exist.") from exc

        if not getattr(owner_user, "is_owner", False):
            raise CommandError(f"User '{self.owner_username}' is not an OWNER user.")
        if not getattr(tenant_user, "is_tenant", False):
            raise CommandError(f"User '{self.tenant_username}' is not a TENANT user.")

        try:
            owner_profile = owner_user.rentease_profile
        except UserProfile.DoesNotExist as exc:
            raise CommandError(f"Owner user '{self.owner_username}' has no UserProfile.") from exc

        try:
            tenant = tenant_user.tenant_profile
        except Tenant.DoesNotExist as exc:
            raise CommandError(f"Tenant user '{self.tenant_username}' has no Tenant profile.") from exc

        return owner_user, owner_profile, tenant_user, tenant

    def _print_dry_run(self, owner_user, owner_profile, tenant_user, tenant):
        self.stdout.write("RentEase demo data dry-run. No database writes were performed.")
        self.stdout.write(f"- Owner account: {owner_user.username} / profile: {owner_profile.full_name}")
        self.stdout.write(f"- Tenant account: {tenant_user.username} / tenant: {tenant.full_name}")
        if self.reset_demo_data:
            self.stdout.write("- Would reset command-created DEMO-prefixed data first.")
        self.stdout.write("- Would create/update 5 DEMO rooms for the owner.")
        self.stdout.write("- Would create/update 3 published public listings and 2 internal listings.")
        self.stdout.write("- Would create/update 2 tenants linked through owner contracts.")
        self.stdout.write("- Would create/update 2 active contracts.")
        self.stdout.write("- Would create/update price configs, invoices, invoice details, and payments.")
        self.stdout.write("- Would create/update repair requests, notifications, and viewing registrations.")

    def _reset_demo_data(self, owner_profile, tenant):
        demo_rooms = Room.objects.filter(owner=owner_profile, room_code__startswith=DEMO_PREFIX)
        demo_contracts = Contract.objects.filter(contract_code__startswith=DEMO_PREFIX)
        demo_invoices = Invoice.objects.filter(invoice_code__startswith=f"INV-DEMO-")
        demo_repairs = RepairRequest.objects.filter(title__startswith=DEMO_PREFIX)
        demo_listings = RoomListing.objects.filter(title__startswith=DEMO_PREFIX)
        demo_viewings = ViewingRegistration.objects.filter(full_name__startswith=DEMO_PREFIX)
        demo_notifications = Notification.objects.filter(title__startswith=DEMO_PREFIX)
        demo_payments = PaymentHistory.objects.filter(transaction_code__startswith=DEMO_PREFIX)
        demo_tenants = Tenant.objects.filter(citizen_id__startswith=DEMO_PREFIX, account__isnull=True)

        deleted_counts = {}
        for label, queryset in [
            ("notifications", demo_notifications),
            ("payments", demo_payments),
            ("invoice details", InvoiceDetail.objects.filter(invoice__in=demo_invoices)),
            ("invoices", demo_invoices),
            ("repairs", demo_repairs),
            ("viewing registrations", demo_viewings),
            ("listings", demo_listings),
            ("contracts", demo_contracts),
            ("price configs", PriceConfig.objects.filter(room__in=demo_rooms)),
            ("rooms", demo_rooms),
            ("demo-only tenants", demo_tenants),
        ]:
            count = queryset.count()
            queryset.delete()
            deleted_counts[label] = count

        self.actions.append(
            "Reset demo data: "
            + ", ".join(f"{label}={count}" for label, count in deleted_counts.items())
        )

    def _seed(self, owner_user, owner_profile, tenant_user, tenant):
        today = timezone.localdate()
        month = today.month
        year = today.year
        month_start = date(year, month, 1)
        contract_end = today + timedelta(days=330)
        ending_soon = today + timedelta(days=25)

        tenant = self._prepare_primary_tenant(tenant)
        second_tenant = self._upsert_second_tenant()
        rooms = self._upsert_rooms(owner_profile)
        self._upsert_listings(rooms, today)
        contracts = self._upsert_contracts(rooms, tenant, second_tenant, today, contract_end, ending_soon)
        invoices = self._upsert_billing(owner_user, rooms, contracts, month, year, month_start, today)
        repairs = self._upsert_repairs(rooms, tenant)
        self._upsert_notifications(tenant, invoices["tenant_invoice"], repairs["pending"])
        self._upsert_viewing_registrations(rooms, tenant, today)

        self.actions.append("Seeded demo rooms, listings, contracts, billing, repairs, notifications, and viewings.")

    def _prepare_primary_tenant(self, tenant):
        tenant.full_name = "Demo Tenant"
        tenant.email = "tenant.demo@example.test"
        tenant.phone_number = "0900000002"
        tenant.citizen_id = "DEMO-TENANT-001"
        tenant.address = "Demo Tenant Address"
        tenant.status = "active"
        tenant.citizen_id_front = None
        tenant.citizen_id_back = None
        tenant.full_clean()
        tenant.save()
        self.actions.append("Verified tenant_test profile as fake demo tenant.")
        return tenant

    def _upsert_second_tenant(self):
        tenant, _created = Tenant.objects.update_or_create(
            citizen_id="DEMO-TENANT-002",
            defaults={
                "account": None,
                "full_name": "Demo Roommate",
                "email": "roommate.demo@example.test",
                "phone_number": "0900000003",
                "address": "Demo Roommate Address",
                "gender": "other",
                "status": "active",
                "citizen_id_front": None,
                "citizen_id_back": None,
            },
        )
        return tenant

    def _upsert_rooms(self, owner_profile):
        room_specs = [
            ("DEMO-R001", "Phong Studio Demo", "occupied", Decimal("3500000.00"), 1, Decimal("24.00"), 2),
            ("DEMO-R002", "Phong Gac Lung Demo", "occupied", Decimal("3200000.00"), 1, Decimal("28.00"), 2),
            ("DEMO-R003", "Phong Ban Cong Demo", "available", Decimal("2800000.00"), 2, Decimal("22.00"), 2),
            ("DEMO-R004", "Phong Yen Tinh Demo", "available", Decimal("2500000.00"), 2, Decimal("20.00"), 1),
            ("DEMO-R005", "Phong Gan Cong Demo", "available", Decimal("2200000.00"), 3, Decimal("18.00"), 1),
        ]
        rooms = {}
        for code, name, status, rent, floor, area, max_occupants in room_specs:
            room, _created = Room.objects.update_or_create(
                owner=owner_profile,
                room_code=code,
                defaults={
                    "room_name": name,
                    "status": status,
                    "default_rent": rent,
                    "floor": floor,
                    "area": area,
                    "max_occupants": max_occupants,
                    "description": f"{name} for RentEase local demo data.",
                    "room_image": None,
                },
            )
            rooms[code] = room
        return rooms

    def _upsert_listings(self, rooms, today):
        listing_specs = [
            ("DEMO-LIST-R001", rooms["DEMO-R001"], "rented", Decimal("3500000.00")),
            ("DEMO-LIST-R002", rooms["DEMO-R002"], "hidden", Decimal("3200000.00")),
            ("DEMO-LIST-R003", rooms["DEMO-R003"], "published", Decimal("2800000.00")),
            ("DEMO-LIST-R004", rooms["DEMO-R004"], "published", Decimal("2500000.00")),
            ("DEMO-LIST-R005", rooms["DEMO-R005"], "published", Decimal("2200000.00")),
        ]
        for title, room, status, price in listing_specs:
            listing = RoomListing.objects.filter(room=room, title=title).first()
            if not listing:
                listing = RoomListing(room=room, title=title)
            listing.description = f"{room.room_name} with clear demo details for public browsing."
            listing.listing_price = price
            listing.deposit_amount = price
            listing.status = status
            listing.available_from = today
            listing.expired_at = None
            listing.image_url = ""
            listing.save()

    def _upsert_contracts(self, rooms, tenant, second_tenant, today, contract_end, ending_soon):
        specs = [
            ("DEMO-CTR-001", rooms["DEMO-R001"], tenant, today - timedelta(days=35), contract_end, "active"),
            ("DEMO-CTR-002", rooms["DEMO-R002"], second_tenant, today - timedelta(days=120), ending_soon, "active"),
        ]
        contracts = {}
        for code, room, tenant_obj, start_date, end_date, status in specs:
            contract, _created = Contract.objects.update_or_create(
                contract_code=code,
                defaults={
                    "room": room,
                    "tenant": tenant_obj,
                    "previous_contract": None,
                    "signed_date": start_date,
                    "start_date": start_date,
                    "end_date": end_date,
                    "rent_amount": room.default_rent,
                    "deposit_amount": room.default_rent,
                    "payment_cycle": "monthly",
                    "status": status,
                },
            )
            contracts[code] = contract
        return contracts

    def _upsert_billing(self, owner_user, rooms, contracts, month, year, month_start, today):
        tenant_invoice = self._upsert_invoice_set(
            owner_user=owner_user,
            contract=contracts["DEMO-CTR-001"],
            room=rooms["DEMO-R001"],
            month=month,
            year=year,
            month_start=month_start,
            today=today,
            electricity_start=120,
            electricity_end=165,
            water_start=30,
            water_end=42,
            payment_code="DEMO-PAY-001",
            payment_mode="partial",
        )
        paid_invoice = self._upsert_invoice_set(
            owner_user=owner_user,
            contract=contracts["DEMO-CTR-002"],
            room=rooms["DEMO-R002"],
            month=month,
            year=year,
            month_start=month_start,
            today=today,
            electricity_start=210,
            electricity_end=250,
            water_start=55,
            water_end=68,
            payment_code="DEMO-PAY-002",
            payment_mode="full",
        )
        return {
            "tenant_invoice": tenant_invoice,
            "paid_invoice": paid_invoice,
        }

    def _upsert_invoice_set(
        self,
        owner_user,
        contract,
        room,
        month,
        year,
        month_start,
        today,
        electricity_start,
        electricity_end,
        water_start,
        water_end,
        payment_code,
        payment_mode,
    ):
        PriceConfig.objects.update_or_create(
            room=room,
            month=month,
            year=year,
            defaults={
                "electricity_unit_price": Decimal("3500.00"),
                "water_unit_price": Decimal("15000.00"),
                "service_fee": Decimal("150000.00"),
                "effective_from": month_start,
            },
        )

        invoice_code = f"INV-DEMO-{contract.contract_code}"
        invoice, _created = Invoice.objects.update_or_create(
            contract=contract,
            month=month,
            year=year,
            defaults={
                "invoice_code": invoice_code,
                "issued_date": today,
                "due_date": today + timedelta(days=7),
                "note": "DEMO invoice for RentEase local walkthrough.",
            },
        )
        invoice.full_clean()
        invoice.save()

        detail, _created = InvoiceDetail.objects.get_or_create(
            invoice=invoice,
            defaults={
                "electricity_start": electricity_start,
                "electricity_end": electricity_end,
                "water_start": water_start,
                "water_end": water_end,
            },
        )
        detail.electricity_start = electricity_start
        detail.electricity_end = electricity_end
        detail.water_start = water_start
        detail.water_end = water_end
        detail.save()
        invoice.refresh_from_db()

        if payment_mode == "partial":
            amount = (invoice.total_amount * Decimal("0.50")).quantize(Decimal("0.01"))
        else:
            amount = invoice.total_amount

        payment = PaymentHistory.objects.filter(transaction_code=payment_code).first()
        if not payment:
            payment = PaymentHistory(invoice=invoice, transaction_code=payment_code)
        payment.invoice = invoice
        payment.amount = amount
        payment.method = PaymentHistory.METHOD_BANK_TRANSFER
        payment.paid_at = timezone.make_aware(datetime.combine(today, time(9, 30)))
        payment.collector = owner_user
        payment.note = "DEMO payment for local walkthrough."
        payment.save()
        invoice.refresh_from_db()
        return invoice

    def _upsert_repairs(self, rooms, tenant):
        pending = self._upsert_repair(
            room=rooms["DEMO-R001"],
            tenant=tenant,
            title="DEMO-REPAIR-001 Leaking faucet",
            description="Demo repair request for a leaking faucet in the bathroom.",
            priority=RepairRequest.PRIORITY_HIGH,
            status=RepairRequest.STATUS_PENDING,
        )
        completed = self._upsert_repair(
            room=rooms["DEMO-R001"],
            tenant=tenant,
            title="DEMO-REPAIR-002 Light replacement",
            description="Demo completed repair request for replacing a room light.",
            priority=RepairRequest.PRIORITY_MEDIUM,
            status=RepairRequest.STATUS_COMPLETED,
        )
        return {
            "pending": pending,
            "completed": completed,
        }

    def _upsert_repair(self, room, tenant, title, description, priority, status):
        repair = RepairRequest.objects.filter(room=room, tenant=tenant, title=title).first()
        if not repair:
            repair = RepairRequest(room=room, tenant=tenant, title=title)
        repair.description = description
        repair.priority = priority
        repair.status = status
        repair.image = None
        repair.owner_note = "DEMO owner note for local walkthrough." if status == RepairRequest.STATUS_COMPLETED else ""
        repair.save()
        return repair

    def _upsert_notifications(self, tenant, invoice, repair):
        notification_specs = [
            (
                "DEMO-NOTIFY-001 Invoice ready",
                "Your demo invoice is ready for review.",
                Notification.TYPE_INVOICE,
                invoice,
                None,
            ),
            (
                "DEMO-NOTIFY-002 Repair received",
                "Your demo repair request has been received by the owner.",
                Notification.TYPE_REPAIR,
                None,
                repair,
            ),
        ]
        for title, message, notification_type, invoice_obj, repair_obj in notification_specs:
            notification = Notification.objects.filter(tenant=tenant, title=title).first()
            if not notification:
                notification = Notification(tenant=tenant, title=title)
            notification.message = message
            notification.notification_type = notification_type
            notification.invoice = invoice_obj
            notification.repair_request = repair_obj
            notification.is_read = False
            notification.save()

    def _upsert_viewing_registrations(self, rooms, tenant, today):
        listing_one = RoomListing.objects.get(room=rooms["DEMO-R003"], title="DEMO-LIST-R003")
        listing_two = RoomListing.objects.get(room=rooms["DEMO-R004"], title="DEMO-LIST-R004")
        listing_three = RoomListing.objects.get(room=rooms["DEMO-R005"], title="DEMO-LIST-R005")

        specs = [
            (listing_one, None, "DEMO-VISITOR-001 Demo Visitor One", "0900000101", "visitor.one@example.test", "pending"),
            (listing_two, None, "DEMO-VISITOR-002 Demo Visitor Two", "0900000102", "visitor.two@example.test", "confirmed"),
            (listing_three, tenant, "DEMO-VISITOR-003 Demo Tenant Visit", "0900000002", "tenant.demo@example.test", "completed"),
        ]
        for listing, tenant_obj, full_name, phone, email, status in specs:
            registration = ViewingRegistration.objects.filter(listing=listing, full_name=full_name).first()
            if not registration:
                registration = ViewingRegistration(listing=listing, full_name=full_name)
            registration.tenant = tenant_obj
            registration.phone = phone
            registration.email = email
            registration.preferred_date = today + timedelta(days=3)
            registration.preferred_time = time(10, 0)
            registration.status = status
            registration.note = "DEMO viewing registration for local walkthrough."
            registration.admin_note = "DEMO internal viewing note."
            registration.save()
