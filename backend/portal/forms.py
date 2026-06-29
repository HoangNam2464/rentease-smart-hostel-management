from django import forms
from django.contrib.auth.forms import AuthenticationForm

from billing.models import Invoice, PaymentHistory
from contracts.models import Contract
from listings.models import RoomListing, ViewingRegistration
from maintenance.models import RepairRequest
from properties.models import Room
from tenants.models import Tenant


class RentEaseAuthenticationForm(AuthenticationForm):
    """Login form for the RentEase role-based portal."""

    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': (
            'Tên đăng nhập hoặc mật khẩu chưa đúng. Vui lòng kiểm tra và thử lại.'
        ),
    }


class OwnerRoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
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

    def clean_room_code(self):
        room_code = self.cleaned_data['room_code']
        if self.owner_profile and Room.objects.filter(
            owner=self.owner_profile,
            room_code=room_code,
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This owner already has a room with this room code.')
        return room_code

    def clean_max_occupants(self):
        max_occupants = self.cleaned_data['max_occupants']
        if max_occupants < 1:
            raise forms.ValidationError('Ensure this value is greater than or equal to 1.')
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
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
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
            'signed_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
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
            'signed_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
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
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
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
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
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
            'available_from': forms.DateInput(attrs={'type': 'date'}),
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
