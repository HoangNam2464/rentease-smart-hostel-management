from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Q
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
        self.stdout.write(f"- Owner account: {owner_user.username} / linked owner profile found.")
        self.stdout.write(f"- Tenant account: {tenant_user.username} / linked tenant record found.")
        if self.reset_demo_data:
            self.stdout.write("- Would reset command-created DEMO-prefixed data first.")
        self.stdout.write("- Would create/update 5 realistic Vietnamese demo rooms for the owner.")
        self.stdout.write("- Would create/update 3 published public listings and 2 internal listings with Vietnamese copy.")
        self.stdout.write("- Would create/update 2 fake tenants linked through owner contracts.")
        self.stdout.write("- Would create/update 2 active contracts with realistic contract codes.")
        self.stdout.write("- Would create/update price configs, invoices, invoice details, and payments.")
        self.stdout.write("- Would create/update realistic repair requests, notifications, and viewing registrations.")

    def _reset_demo_data(self, owner_profile, tenant):
        demo_rooms = Room.objects.filter(owner=owner_profile, room_code__startswith=DEMO_PREFIX)
        demo_contracts = Contract.objects.filter(
            Q(contract_code__startswith=DEMO_PREFIX) | Q(room__in=demo_rooms)
        )
        demo_invoices = Invoice.objects.filter(
            Q(invoice_code__startswith="INV-DEMO-") | Q(contract__in=demo_contracts)
        )
        demo_repairs = RepairRequest.objects.filter(
            Q(title__startswith=DEMO_PREFIX) | Q(room__in=demo_rooms, tenant=tenant)
        )
        demo_listings = RoomListing.objects.filter(
            Q(title__startswith=DEMO_PREFIX) | Q(room__in=demo_rooms)
        )
        demo_viewings = ViewingRegistration.objects.filter(
            Q(full_name__startswith=DEMO_PREFIX) | Q(listing__in=demo_listings)
        )
        demo_notifications = Notification.objects.filter(
            Q(title__startswith=DEMO_PREFIX)
            | Q(tenant=tenant, invoice__in=demo_invoices)
            | Q(tenant=tenant, repair_request__in=demo_repairs)
        )
        demo_payments = PaymentHistory.objects.filter(
            Q(transaction_code__startswith=DEMO_PREFIX) | Q(invoice__in=demo_invoices)
        )
        demo_tenants = Tenant.objects.filter(
            Q(citizen_id__startswith=DEMO_PREFIX) | Q(citizen_id="FAKE-ID-VY-002"),
            account__isnull=True,
        )

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

        owner_profile = self._prepare_owner_profile(owner_profile)
        tenant = self._prepare_primary_tenant(tenant)
        second_tenant = self._upsert_second_tenant()
        rooms = self._upsert_rooms(owner_profile)
        self._upsert_listings(rooms, today)
        contracts = self._upsert_contracts(rooms, tenant, second_tenant, today, contract_end, ending_soon)
        invoices = self._upsert_billing(owner_user, rooms, contracts, month, year, month_start, today)
        repairs = self._upsert_repairs(rooms, tenant)
        self._upsert_notifications(tenant, invoices["tenant_invoice"], repairs["pending"])
        self._upsert_viewing_registrations(rooms, tenant, today)

        self.actions.append("Seeded realistic Vietnamese demo data for rooms, listings, contracts, billing, repairs, notifications, and viewings.")

    def _prepare_owner_profile(self, owner_profile):
        owner_profile.full_name = "Nguyễn Minh Anh"
        owner_profile.phone_number = "0901000101"
        owner_profile.gender = "female"
        owner_profile.rental_address = "123 Đường Hoa Sữa, Phường 7, Quận Phú Nhuận, TP. Hồ Chí Minh"
        owner_profile.full_clean()
        owner_profile.save()
        self.actions.append("Verified owner_test profile with realistic Vietnamese display data.")
        return owner_profile

    def _prepare_primary_tenant(self, tenant):
        tenant.full_name = "Trần Hoàng Nam"
        tenant.email = "hoangnam.demo@example.test"
        tenant.phone_number = "0901000202"
        tenant.citizen_id = "FAKE-ID-NAM-001"
        tenant.address = "45 Nguyễn Văn Đậu, Phường 6, Quận Bình Thạnh, TP. Hồ Chí Minh"
        tenant.gender = "male"
        tenant.status = "active"
        tenant.citizen_id_front = None
        tenant.citizen_id_back = None
        tenant.full_clean()
        tenant.save()
        self.actions.append("Verified tenant_test profile with realistic Vietnamese display data.")
        return tenant

    def _upsert_second_tenant(self):
        tenant = Tenant.objects.filter(citizen_id__in=["FAKE-ID-VY-002", "DEMO-TENANT-002"]).first()
        if not tenant:
            tenant = Tenant(citizen_id="FAKE-ID-VY-002")
        tenant.account = None
        tenant.full_name = "Lê Thảo Vy"
        tenant.email = "thaovy.demo@example.test"
        tenant.phone_number = "0901000303"
        tenant.citizen_id = "FAKE-ID-VY-002"
        tenant.address = "12 Lê Quang Định, Phường 14, Quận Bình Thạnh, TP. Hồ Chí Minh"
        tenant.gender = "female"
        tenant.status = "active"
        tenant.citizen_id_front = None
        tenant.citizen_id_back = None
        tenant.full_clean()
        tenant.save()
        return tenant

    def _upsert_rooms(self, owner_profile):
        room_specs = [
            (
                "DEMO-R001",
                "Phòng 101 - Studio có ban công",
                "occupied",
                Decimal("3500000.00"),
                1,
                Decimal("24.00"),
                2,
                "Studio tầng 1 có ban công nhỏ, cửa sổ thoáng, phù hợp người đi làm cần không gian riêng.",
            ),
            (
                "DEMO-R002",
                "Phòng 102 - Studio tiêu chuẩn",
                "occupied",
                Decimal("3200000.00"),
                1,
                Decimal("22.00"),
                2,
                "Studio tiêu chuẩn, có khu bếp nhỏ và nhà vệ sinh riêng, đang có khách thuê ổn định.",
            ),
            (
                "DEMO-R003",
                "Phòng 201 - Phòng gác lửng",
                "available",
                Decimal("2800000.00"),
                2,
                Decimal("23.00"),
                2,
                "Phòng gác lửng sáng, có cửa sổ, phù hợp sinh viên hoặc nhân viên văn phòng.",
            ),
            (
                "DEMO-R004",
                "Phòng 202 - Gác lửng đầy đủ nội thất",
                "available",
                Decimal("2500000.00"),
                2,
                Decimal("20.00"),
                1,
                "Phòng gác lửng có giường, tủ, bàn học và máy lạnh, có thể dọn vào ngay.",
            ),
            (
                "DEMO-R005",
                "Phòng 301 - Phòng rộng cho 2 người",
                "available",
                Decimal("2200000.00"),
                3,
                Decimal("28.00"),
                2,
                "Phòng rộng trên tầng 3, khu vực yên tĩnh, phù hợp hai người ở ghép.",
            ),
        ]
        rooms = {}
        for code, name, status, rent, floor, area, max_occupants, description in room_specs:
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
                    "description": description,
                    "room_image": None,
                },
            )
            rooms[code] = room
        return rooms

    def _upsert_listings(self, rooms, today):
        listing_specs = [
            (
                "Phòng 101 - Studio có ban công",
                rooms["DEMO-R001"],
                "rented",
                Decimal("3500000.00"),
                "Phòng đã có khách thuê, giữ trong dữ liệu demo để minh họa trạng thái đã thuê.",
            ),
            (
                "Phòng 102 - Studio tiêu chuẩn",
                rooms["DEMO-R002"],
                "hidden",
                Decimal("3200000.00"),
                "Tin được ẩn trong demo vì phòng đang có hợp đồng thuê.",
            ),
            (
                "Phòng 201 gác lửng gần chợ, giờ giấc tự do",
                rooms["DEMO-R003"],
                "published",
                Decimal("2800000.00"),
                "Phòng gác lửng thoáng, có bếp riêng, khu dân cư an ninh, phù hợp sinh viên hoặc nhân viên văn phòng.",
            ),
            (
                "Phòng 202 đầy đủ nội thất, dọn vào ở ngay",
                rooms["DEMO-R004"],
                "published",
                Decimal("2500000.00"),
                "Phòng có máy lạnh, giường, tủ quần áo và bàn học. Giá thuê đã bao gồm phí quản lý cơ bản.",
            ),
            (
                "Phòng 301 rộng cho 2 người, khu vực yên tĩnh",
                rooms["DEMO-R005"],
                "published",
                Decimal("2200000.00"),
                "Phòng rộng, cửa sổ lớn, phù hợp hai người ở ghép. Có chỗ để xe và lối đi riêng.",
            ),
        ]
        for title, room, status, price, description in listing_specs:
            listing = RoomListing.objects.filter(room=room).first()
            if not listing:
                listing = RoomListing(room=room, title=title)
            listing.title = title
            listing.description = description
            listing.listing_price = price
            listing.deposit_amount = price
            listing.status = status
            listing.available_from = today
            listing.expired_at = None
            listing.image_url = ""
            listing.save()

    def _upsert_contracts(self, rooms, tenant, second_tenant, today, contract_end, ending_soon):
        specs = [
            ("HD-NT-2026-101", "DEMO-CTR-001", rooms["DEMO-R001"], tenant, today - timedelta(days=35), contract_end, "active"),
            ("HD-NT-2026-102", "DEMO-CTR-002", rooms["DEMO-R002"], second_tenant, today - timedelta(days=120), ending_soon, "active"),
        ]
        contracts = {}
        for code, old_code, room, tenant_obj, start_date, end_date, status in specs:
            contract = Contract.objects.filter(contract_code__in=[code, old_code]).first()
            if not contract:
                contract = Contract.objects.filter(room=room, tenant=tenant_obj).first()
            if not contract:
                contract = Contract(contract_code=code)
            contract.contract_code = code
            contract.room = room
            contract.tenant = tenant_obj
            contract.previous_contract = None
            contract.signed_date = start_date
            contract.start_date = start_date
            contract.end_date = end_date
            contract.rent_amount = room.default_rent
            contract.deposit_amount = room.default_rent
            contract.payment_cycle = "monthly"
            contract.status = status
            contract.full_clean()
            contract.save()
            contracts[code] = contract
        return contracts

    def _upsert_billing(self, owner_user, rooms, contracts, month, year, month_start, today):
        tenant_invoice = self._upsert_invoice_set(
            owner_user=owner_user,
            contract=contracts["HD-NT-2026-101"],
            room=rooms["DEMO-R001"],
            month=month,
            year=year,
            month_start=month_start,
            today=today,
            electricity_start=124,
            electricity_end=168,
            water_start=32,
            water_end=43,
            payment_code="PTT-2026-101-01",
            payment_mode="partial",
        )
        paid_invoice = self._upsert_invoice_set(
            owner_user=owner_user,
            contract=contracts["HD-NT-2026-102"],
            room=rooms["DEMO-R002"],
            month=month,
            year=year,
            month_start=month_start,
            today=today,
            electricity_start=210,
            electricity_end=248,
            water_start=55,
            water_end=66,
            payment_code="PTT-2026-102-01",
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

        invoice_code = f"HDON-{year}{month:02d}-{room.room_code.replace('DEMO-', '')}"
        invoice, _created = Invoice.objects.update_or_create(
            contract=contract,
            month=month,
            year=year,
            defaults={
                "invoice_code": invoice_code,
                "issued_date": today,
                "due_date": today + timedelta(days=7),
                "note": "Hóa đơn tiền phòng, điện, nước và phí dịch vụ cho tháng hiện tại.",
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

        payment = PaymentHistory.objects.filter(
            Q(transaction_code=payment_code) | Q(invoice=invoice, transaction_code__startswith=DEMO_PREFIX)
        ).first()
        if not payment:
            payment = PaymentHistory(invoice=invoice, transaction_code=payment_code)
        payment.invoice = invoice
        payment.transaction_code = payment_code
        payment.amount = amount
        payment.method = PaymentHistory.METHOD_BANK_TRANSFER
        payment.paid_at = timezone.make_aware(datetime.combine(today, time(9, 30)))
        payment.collector = owner_user
        payment.note = "Thanh toán qua chuyển khoản ngân hàng trong dữ liệu demo."
        payment.save()
        invoice.refresh_from_db()
        return invoice

    def _upsert_repairs(self, rooms, tenant):
        pending = self._upsert_repair(
            room=rooms["DEMO-R001"],
            tenant=tenant,
            title="Máy lạnh không lạnh",
            description="Khách thuê báo máy lạnh chạy nhưng không đủ lạnh, cần kiểm tra gas và vệ sinh dàn lạnh.",
            priority=RepairRequest.PRIORITY_HIGH,
            status=RepairRequest.STATUS_PENDING,
        )
        completed = self._upsert_repair(
            room=rooms["DEMO-R001"],
            tenant=tenant,
            title="Vòi nước bị rò",
            description="Vòi nước trong nhà vệ sinh bị rò nhẹ, đã thay ron và kiểm tra lại.",
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
            legacy_title = "DEMO-REPAIR-001 Leaking faucet" if "Máy lạnh" in title else "DEMO-REPAIR-002 Light replacement"
            repair = RepairRequest.objects.filter(room=room, tenant=tenant, title=legacy_title).first()
        if not repair:
            repair = RepairRequest(room=room, tenant=tenant)
        repair.title = title
        repair.description = description
        repair.priority = priority
        repair.status = status
        repair.image = None
        repair.owner_note = "Đã xử lý xong và hẹn khách kiểm tra lại." if status == RepairRequest.STATUS_COMPLETED else ""
        repair.save()
        return repair

    def _upsert_notifications(self, tenant, invoice, repair):
        notification_specs = [
            (
                "Hóa đơn tháng này đã được tạo",
                "Hóa đơn tiền phòng tháng này đã sẵn sàng. Vui lòng kiểm tra số tiền còn lại cần thanh toán.",
                Notification.TYPE_INVOICE,
                invoice,
                None,
            ),
            (
                "Yêu cầu sửa chữa đã được tiếp nhận",
                "Chủ trọ đã nhận yêu cầu sửa chữa máy lạnh và sẽ sắp xếp kiểm tra sớm.",
                Notification.TYPE_REPAIR,
                None,
                repair,
            ),
        ]
        for title, message, notification_type, invoice_obj, repair_obj in notification_specs:
            notification = Notification.objects.filter(tenant=tenant, title=title).first()
            if not notification:
                notification = Notification.objects.filter(
                    tenant=tenant,
                    notification_type=notification_type,
                    invoice=invoice_obj,
                    repair_request=repair_obj,
                ).first()
            if not notification:
                notification = Notification(tenant=tenant)
            notification.title = title
            notification.message = message
            notification.notification_type = notification_type
            notification.invoice = invoice_obj
            notification.repair_request = repair_obj
            notification.is_read = False
            notification.save()

    def _upsert_viewing_registrations(self, rooms, tenant, today):
        listing_one = RoomListing.objects.get(room=rooms["DEMO-R003"])
        listing_two = RoomListing.objects.get(room=rooms["DEMO-R004"])
        listing_three = RoomListing.objects.get(room=rooms["DEMO-R005"])

        specs = [
            (
                listing_one,
                None,
                "Phạm Gia Hân",
                "0901000404",
                "giahan.demo@example.test",
                "pending",
                "Muốn xem phòng sau giờ làm, ưu tiên buổi chiều.",
                "Khách quan tâm phòng gác lửng, cần gọi xác nhận trước khi đến.",
            ),
            (
                listing_two,
                None,
                "Ngô Quốc Bảo",
                "0901000505",
                "quocbao.demo@example.test",
                "confirmed",
                "Đã hẹn xem phòng vào cuối tuần.",
                "Đã xác nhận lịch xem phòng qua điện thoại.",
            ),
            (
                listing_three,
                tenant,
                "Trần Hoàng Nam",
                "0901000202",
                "hoangnam.demo@example.test",
                "completed",
                "Khách thuê muốn tham khảo thêm phòng rộng cho bạn ở ghép.",
                "Lịch xem đã hoàn tất trong dữ liệu demo.",
            ),
        ]
        for listing, tenant_obj, full_name, phone, email, status, note, admin_note in specs:
            registration = ViewingRegistration.objects.filter(listing=listing, phone=phone).first()
            if not registration:
                registration = ViewingRegistration.objects.filter(
                    listing=listing,
                    full_name__startswith=DEMO_PREFIX,
                ).first()
            if not registration:
                registration = ViewingRegistration(listing=listing, full_name=full_name)
            registration.full_name = full_name
            registration.tenant = tenant_obj
            registration.phone = phone
            registration.email = email
            registration.preferred_date = today + timedelta(days=3)
            registration.preferred_time = time(10, 0)
            registration.status = status
            registration.note = note
            registration.admin_note = admin_note
            registration.save()
