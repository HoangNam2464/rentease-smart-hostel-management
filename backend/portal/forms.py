from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone

from billing.models import Invoice, PaymentHistory
from contracts.models import Contract
from listings.models import RoomListing, ViewingRegistration
from maintenance.models import RepairRequest
from properties.models import Property, Room
from tenants.models import Tenant


class RentEaseAuthenticationForm(AuthenticationForm):
    """Login form for the RentEase role-based portal."""

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': (
            'Tên đăng nhập hoặc mật khẩu chưa đúng. Vui lòng kiểm tra và thử lại.'
        ),
    }


class OwnerPropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'property_code',
            'name',
            'address',
            'ward',
            'province_city',
            'latitude',
            'longitude',
            'contact_phone',
            'status',
            'house_rules',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'house_rules': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, owner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner_profile = owner_profile
        if self.instance and self.instance.pk:
            self.fields['property_code'].disabled = True

    def clean_property_code(self):
        property_code = self.cleaned_data['property_code'].strip()
        if self.owner_profile and Property.objects.filter(
            owner=self.owner_profile,
            property_code=property_code,
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Bạn đã có một cơ sở sử dụng mã này.')
        return property_code


class OwnerRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            'property',
            'room_code',
            'room_name',
            'floor',
            'area',
            'max_occupants',
            'default_rent',
            'status',
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, owner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner_profile = owner_profile
        owner_properties = (
            Property.objects.filter(owner=owner_profile)
            if owner_profile
            else Property.objects.none()
        )
        self.fields['property'].queryset = owner_properties.order_by('property_code')
        self.fields['property'].required = True
        self.fields['property'].error_messages['required'] = 'Hãy chọn cơ sở cho thuê của phòng.'
        self.fields['property'].error_messages['invalid_choice'] = 'Cơ sở đã chọn không thuộc quyền quản lý của bạn.'

    def clean_property(self):
        property_record = self.cleaned_data['property']
        if not self.owner_profile or property_record.owner_id != self.owner_profile.pk:
            raise forms.ValidationError('Cơ sở đã chọn không thuộc quyền quản lý của bạn.')
        return property_record

    def clean_room_code(self):
        room_code = self.cleaned_data['room_code']
        property_record = self.cleaned_data.get('property')
        if property_record and Room.objects.filter(
            property=property_record,
            room_code=room_code,
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Cơ sở này đã có một phòng sử dụng mã này.')
        return room_code

    def clean_max_occupants(self):
        max_occupants = self.cleaned_data['max_occupants']
        if max_occupants < 1:
            raise forms.ValidationError('Số người tối đa phải từ 1 trở lên.')
        return max_occupants


class OwnerTenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = [
            'full_name',
            'email',
            'phone_number',
            'address',
            'date_of_birth',
            'gender',
            'status',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 5}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }


class TenantNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.full_name


class OwnerContractCreateForm(forms.ModelForm):
    tenant = TenantNameChoiceField(queryset=Tenant.objects.none())

    class Meta:
        model = Contract
        fields = [
            'room',
            'tenant',
            'previous_contract',
            'contract_code',
            'signed_date',
            'start_date',
            'end_date',
            'rent_amount',
            'deposit_amount',
            'payment_cycle',
            'status',
        ]
        widgets = {
            'signed_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, owner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner_profile = owner_profile
        owner_rooms = Room.objects.filter(owner=owner_profile) if owner_profile else Room.objects.none()
        owner_tenants = (
            Tenant.objects.filter(contracts__room__owner=owner_profile).distinct()
            if owner_profile
            else Tenant.objects.none()
        )
        owner_contracts = (
            Contract.objects.filter(room__owner=owner_profile)
            if owner_profile
            else Contract.objects.none()
        )
        self.fields['room'].queryset = owner_rooms.order_by('room_code')
        self.fields['tenant'].queryset = owner_tenants.order_by('full_name')
        self.fields['previous_contract'].queryset = owner_contracts.order_by('-start_date', 'contract_code')
        self.fields['previous_contract'].required = False


class OwnerContractUpdateForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            'previous_contract',
            'contract_code',
            'signed_date',
            'start_date',
            'end_date',
            'rent_amount',
            'deposit_amount',
            'payment_cycle',
            'status',
        ]
        widgets = {
            'signed_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'start_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'end_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def __init__(self, *args, owner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        owner_contracts = (
            Contract.objects.filter(room__owner=owner_profile)
            if owner_profile
            else Contract.objects.none()
        )
        if self.instance and self.instance.pk:
            owner_contracts = owner_contracts.exclude(pk=self.instance.pk)
        self.fields['previous_contract'].queryset = owner_contracts.order_by('-start_date', 'contract_code')
        self.fields['previous_contract'].required = False


class OwnerInvoiceValidationMixin:
    def clean_month(self):
        month = self.cleaned_data['month']
        if month < 1 or month > 12:
            raise forms.ValidationError('Enter a valid month from 1 to 12.')
        return month

    def clean_year(self):
        year = self.cleaned_data['year']
        if year < 2000:
            raise forms.ValidationError('Enter a valid year greater than or equal to 2000.')
        return year


class OwnerInvoiceCreateForm(OwnerInvoiceValidationMixin, forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'contract',
            'month',
            'year',
            'issued_date',
            'due_date',
            'note',
        ]
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'due_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'note': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, owner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        owner_contracts = (
            Contract.objects.filter(room__owner=owner_profile)
            if owner_profile
            else Contract.objects.none()
        )
        self.fields['contract'].queryset = owner_contracts.order_by('-start_date', 'contract_code')


class OwnerInvoiceUpdateForm(OwnerInvoiceValidationMixin, forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'month',
            'year',
            'issued_date',
            'due_date',
            'note',
        ]
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'due_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'note': forms.Textarea(attrs={'rows': 5}),
        }


class OwnerPaymentCreateForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = [
            'amount',
            'method',
            'transaction_code',
            'paid_at',
            'note',
        ]
        widgets = {
            'paid_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'note': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, invoice=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice = invoice
        if self.invoice:
            self.instance.invoice = self.invoice
        self.fields['paid_at'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M']

    def _post_clean(self):
        if self.invoice:
            self.instance.invoice = self.invoice
        if self.errors.get('amount'):
            return
        super()._post_clean()

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Payment amount must be greater than zero.')

        if not self.invoice:
            raise forms.ValidationError('Invoice is required before recording a payment.')

        if self.invoice.total_amount <= 0:
            raise forms.ValidationError('Cannot record a payment for a zero-total invoice.')

        if self.invoice.remaining_amount <= 0:
            raise forms.ValidationError('This invoice is already fully paid.')

        if amount > self.invoice.remaining_amount:
            raise forms.ValidationError('Payment amount cannot exceed invoice remaining amount.')

        return amount


class TenantRepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['room', 'title', 'description', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, allowed_rooms=None, **kwargs):
        super().__init__(*args, **kwargs)
        room_model = RepairRequest._meta.get_field('room').remote_field.model
        self.allowed_rooms = allowed_rooms if allowed_rooms is not None else room_model.objects.none()
        self.fields['room'].queryset = self.allowed_rooms
        self.fields['room'].required = True
        self.fields['title'].required = True
        self.fields['description'].required = True
        self.fields['priority'].required = True

    def clean_room(self):
        room = self.cleaned_data['room']
        if not self.allowed_rooms.filter(pk=room.pk).exists():
            raise forms.ValidationError('Selected room is not linked to your active contracts.')
        return room


class OwnerRepairProcessForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ['status', 'owner_note']
        widgets = {
            'owner_note': forms.Textarea(attrs={'rows': 5}),
        }

    def clean_status(self):
        status = self.cleaned_data['status']
        if status not in dict(RepairRequest.STATUS_CHOICES):
            raise forms.ValidationError('Selected status is not valid.')

        if (
            self.instance
            and self.instance.pk
            and self.instance.resolved_at
            and self.instance.status == RepairRequest.STATUS_COMPLETED
            and status != RepairRequest.STATUS_COMPLETED
        ):
            raise forms.ValidationError('Completed repair requests cannot be moved back to a non-completed status.')

        return status


class OwnerRoomListingForm(forms.ModelForm):
    class Meta:
        model = RoomListing
        fields = [
            'room',
            'title',
            'description',
            'listing_price',
            'deposit_amount',
            'status',
            'available_from',
            'expired_at',
            'image_url',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'available_from': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'expired_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, allowed_rooms=None, **kwargs):
        super().__init__(*args, **kwargs)
        room_model = RoomListing._meta.get_field('room').remote_field.model
        self.allowed_rooms = allowed_rooms if allowed_rooms is not None else room_model.objects.none()
        self.fields['room'].queryset = self.allowed_rooms
        self.fields['room'].required = True
        self.fields['expired_at'].input_formats = ['%Y-%m-%dT%H:%M']

    def clean_room(self):
        room = self.cleaned_data['room']
        if not self.allowed_rooms.filter(pk=room.pk).exists():
            raise forms.ValidationError('Selected room is not linked to your owner profile.')
        return room


class OwnerViewingRegistrationProcessForm(forms.Form):
    status = forms.ChoiceField(choices=ViewingRegistration.STATUS_CHOICES)
    admin_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 5}),
    )

    def clean_status(self):
        status = self.cleaned_data['status']
        if status not in dict(ViewingRegistration.STATUS_CHOICES):
            raise forms.ValidationError('Selected status is not valid.')
        return status


class OwnerTenantOnboardingForm(UserCreationForm):
    full_name = forms.CharField(label='Họ và tên', max_length=150)
    phone_number = forms.CharField(label='Số điện thoại', max_length=15)
    contract_code = forms.CharField(label='Mã hợp đồng', max_length=50)
    signed_date = forms.DateField(label='Ngày ký', widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    start_date = forms.DateField(label='Ngày bắt đầu', widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    end_date = forms.DateField(label='Ngày kết thúc', widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'))
    rent_amount = forms.DecimalField(
        label='Tiền thuê mỗi kỳ', max_digits=12, decimal_places=2, min_value=0
    )
    deposit_amount = forms.DecimalField(
        label='Tiền cọc', max_digits=12, decimal_places=2, min_value=0, initial=0
    )
    payment_cycle = forms.ChoiceField(
        label='Chu kỳ thanh toán', choices=Contract.PAYMENT_CYCLE_CHOICES, initial='monthly'
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')
        labels = {'username': 'Tên đăng nhập', 'email': 'Email đăng nhập'}

    def __init__(self, *args, registration=None, owner_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration = registration
        self.owner_profile = owner_profile
        self.fields['email'].required = False
        self.fields['password1'].label = 'Mật khẩu tạm thời'
        self.fields['password2'].label = 'Nhập lại mật khẩu'

        if registration and not self.is_bound:
            today = timezone.localdate()
            start_date = max(today, registration.listing.available_from)
            self.fields['full_name'].initial = registration.full_name
            self.fields['phone_number'].initial = registration.phone
            self.fields['email'].initial = registration.email or ''
            self.fields['contract_code'].initial = f'HD-{today.year}-{registration.pk:04d}'
            self.fields['signed_date'].initial = today
            self.fields['start_date'].initial = start_date
            self.fields['end_date'].initial = start_date + timedelta(days=365)
            self.fields['rent_amount'].initial = registration.listing.listing_price
            self.fields['deposit_amount'].initial = registration.listing.deposit_amount

    def clean_contract_code(self):
        contract_code = self.cleaned_data['contract_code'].strip()
        if Contract.objects.filter(contract_code=contract_code).exists():
            raise forms.ValidationError('Mã hợp đồng này đã tồn tại.')
        return contract_code

    def clean(self):
        cleaned_data = super().clean()
        registration = self.registration
        owner_profile = self.owner_profile

        if not registration or not owner_profile:
            raise forms.ValidationError('Không thể xác định lịch xem phòng cần onboarding.')

        listing = registration.listing
        room = listing.room
        allowed_statuses = {
            ViewingRegistration.STATUS_CONFIRMED,
            ViewingRegistration.STATUS_COMPLETED,
        }

        if room.owner_id != owner_profile.pk:
            raise forms.ValidationError('Bạn không có quyền onboarding khách cho phòng này.')
        if registration.tenant_id:
            raise forms.ValidationError('Lịch xem này đã được liên kết với một người thuê.')
        if registration.status not in allowed_statuses:
            raise forms.ValidationError('Hãy xác nhận hoặc hoàn tất lịch xem trước khi tạo tài khoản.')
        if listing.status != RoomListing.STATUS_PUBLISHED:
            raise forms.ValidationError('Tin phòng không còn ở trạng thái đang đăng.')
        if room.status != 'available':
            raise forms.ValidationError('Phòng không còn ở trạng thái còn trống.')
        if Contract.objects.filter(room=room, status='active').exists():
            raise forms.ValidationError('Phòng này đã có hợp đồng đang hoạt động.')

        signed_date = cleaned_data.get('signed_date')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and start_date < listing.available_from:
            self.add_error('start_date', 'Ngày bắt đầu không được trước ngày phòng sẵn sàng.')
        if start_date and end_date and end_date < start_date:
            self.add_error('end_date', 'Ngày kết thúc phải từ ngày bắt đầu trở đi.')
        if signed_date and end_date and signed_date > end_date:
            self.add_error('signed_date', 'Ngày ký không được sau ngày kết thúc hợp đồng.')

        return cleaned_data
