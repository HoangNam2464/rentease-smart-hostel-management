# RentEase Demo Checklist

## Pre-demo Checks

- Pull latest `main`.
- Confirm working tree is clean.
- Run `python manage.py check`.
- Run `python manage.py makemigrations --check --dry-run`.
- Start the server.

## Admin Login Check

- Open `/admin/`.
- Login with demo superuser.
- Confirm RentEase apps are visible.
- Open `/reports/`.

## Data Creation Checklist

- Create owner user.
- Create owner profile.
- Create room.
- Create tenant.
- Create contract.

## Billing Checklist

- Create price config.
- Create invoice.
- Add invoice detail with meter readings.
- Confirm calculated total.
- Record partial payment.
- Record full payment.
- Confirm invoice status is paid.

## Maintenance Checklist

- Create repair request.
- Mark repair request in progress.
- Mark repair request completed.
- Create maintenance record.
- Create notification.

## Listing Checklist

- Create room listing.
- Publish room listing.
- Create viewing registration.
- Confirm viewing registration.
- Mark viewing registration completed or no-show.

## Reports Checklist

- Open dashboard.
- Open billing report.
- Open room report.
- Open tenant/contract report.
- Open maintenance report.
- Open listing/viewing report.

## Final Verification Checklist

- No Django errors.
- No pending migrations.
- Demo data uses fake information only.
- No `.env`, `db.sqlite3`, or `backup_phase*.json` committed for public submission.
