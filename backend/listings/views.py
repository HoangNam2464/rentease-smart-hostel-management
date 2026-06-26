from django.contrib import messages
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
    return render(request, 'listings/public_listing_list.html', {
        'listings': listings,
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
