from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ViewingRegistrationForm
from .models import RoomListing


def published_listings():
    return (
        RoomListing.objects
        .select_related('room')
        .filter(status=RoomListing.STATUS_PUBLISHED)
    )


def public_listing_list(request):
    listings = published_listings()

    query = request.GET.get('q', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    order = request.GET.get('order', 'newest')

    if query:
        listings = listings.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(room__room_name__icontains=query)
        )

    if max_price:
        try:
            parsed_max_price = Decimal(max_price)
        except InvalidOperation:
            max_price = ''
        else:
            if parsed_max_price.is_finite() and parsed_max_price >= 0:
                listings = listings.filter(listing_price__lte=parsed_max_price)
            else:
                max_price = ''

    ordering = {
        'price_asc': ('listing_price', '-created_at'),
        'price_desc': ('-listing_price', '-created_at'),
        'newest': ('-created_at',),
    }
    if order not in ordering:
        order = 'newest'
    listings = listings.order_by(*ordering[order])

    return render(request, 'listings/public_listing_list.html', {
        'listings': listings,
        'filters': {
            'q': query,
            'max_price': max_price,
            'order': order,
        },
    })


def public_listing_detail(request, pk):
    listing = get_object_or_404(published_listings(), pk=pk)
    return render(request, 'listings/public_listing_detail.html', {
        'listing': listing,
    })


def viewing_registration_create(request, pk):
    listing = get_object_or_404(published_listings(), pk=pk)
    form = ViewingRegistrationForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        registration = form.save(commit=False)
        registration.listing = listing
        registration.save()
        messages.success(request, 'Your viewing registration has been submitted.')
        return redirect('listings:viewing_registration_success', pk=listing.pk)

    return render(request, 'listings/viewing_registration_form.html', {
        'listing': listing,
        'form': form,
    })


def viewing_registration_success(request, pk):
    listing = get_object_or_404(published_listings(), pk=pk)
    return render(request, 'listings/viewing_registration_success.html', {
        'listing': listing,
    })
