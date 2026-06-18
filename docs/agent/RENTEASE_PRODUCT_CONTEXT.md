# RentEase Product Context

## Product Target

RentEase is intended to become a real production-ready boarding-house management system, not only a local demo.

The system should eventually support:

- secure production settings
- production database
- owner-facing billing details and utility/service charges
- proper account lifecycle
- owner tenant creation/onboarding
- deployment-ready static/media/email/logging
- clean legacy isolation or removal
- strong owner/tenant data isolation

## Product Vision

RentEase is a Django-based hostel/boarding-house management system. It started from the original HOSTELLO project, so legacy HOSTELLO apps still exist in the repository.

RentEase should be the main product surface. Legacy HOSTELLO should not be part of the production user flow.

## Core Users

Visitor/Public:

- browse published rooms
- view public-safe room details
- submit viewing registrations

Owner:

- manage own rooms
- manage own listings
- manage own linked tenants
- manage own contracts
- manage own invoices
- record payments
- handle repair requests
- process viewing registrations
- view owner dashboard metrics

Tenant:

- view own profile
- view own contracts
- view own invoices
- view own payments
- submit and view own repair requests
- view own notifications

Admin/Staff:

- manage system-wide data through Django Admin
- view staff-only reports
- supervise data consistency and operational records

## Current Product Direction

The project has moved beyond a simple school demo. It is now being hardened toward a real web application.

Production standard requires:

- secure settings
- production database
- no root legacy exposure
- complete owner-facing billing
- account lifecycle
- deployment-ready static/media/email/logging

## Legacy Context

The original HOSTELLO apps are still present. They must not be deleted unless explicitly approved.

Legacy routes should remain isolated. Root-level legacy exposure must not be reintroduced.

Allowed legacy routes at the current state:

- `/legacy/`
- `/legacy/login/`

Do not add `/legacy/api/` or `/legacy/fees/` unless explicitly approved.
