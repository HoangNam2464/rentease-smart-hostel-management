# RentEase Demo Script

Use Django Admin for the final MVP demo.

## Demo Flow

1. Login admin
   - Open `/admin/`
   - Login with the demo superuser.

2. Create Owner user
   - Go to Accounts > Users.
   - Create a user with role `OWNER`.

3. Create Owner Profile
   - Go to Accounts > Owner Profiles.
   - Link the profile to the owner user.

4. Create Room
   - Go to Properties > Rooms.
   - Select owner profile.
   - Fill room code, room name, default rent, capacity, and status.

5. Create Tenant
   - Go to Tenants > Tenants.
   - Fill tenant name, phone, email, citizen ID, and status.

6. Create Contract
   - Go to Contracts > Contracts.
   - Select room and tenant.
   - Fill contract code, signed date, start date, end date, rent, deposit, payment cycle, and status.

7. Create PriceConfig
   - Go to Billing > Price Configs.
   - Select room, month, year, electricity price, water price, and service fee.

8. Generate Invoice and InvoiceDetail
   - Go to Billing > Invoices.
   - Select contract, month, year, issued date, due date.
   - Add invoice detail with electricity and water readings.
   - Confirm total amount is calculated.

9. Record partial payment
   - Add a Payment History row under the invoice.
   - Enter amount lower than remaining debt.
   - Confirm invoice status changes to partial.

10. Record full payment
   - Add another Payment History row for the remaining debt.
   - Confirm invoice status changes to paid and remaining amount is zero.

11. Create RepairRequest
   - Go to Maintenance > Repair Requests.
   - Select room and tenant.
   - Fill title, description, priority, and status.

12. Create MaintenanceRecord
   - Go to Maintenance > Maintenance Records.
   - Select room and optional repair request.
   - Fill maintenance type, description, vendor, cost, performed date, and status.

13. Create Notification
   - Go to Maintenance > Notifications.
   - Create a notification for tenant, invoice, or repair request.

14. Create RoomListing
   - Go to Listings > Room Listings.
   - Select room.
   - Fill title, description, listing price, deposit, available date, and status.
   - Publish the listing.

15. Create ViewingRegistration
   - Go to Listings > Viewing Registrations.
   - Select a published listing.
   - Fill viewer name, phone, email, preferred date/time, and status.

16. Open `/reports/`
   - Use the Reports link or open `/reports/` directly.

17. Show reports
   - Dashboard
   - Billing report
   - Room report
   - Tenant/contract report
   - Maintenance report
   - Listing/viewing report

## Demo Tips

- Use short, realistic demo names.
- Avoid real phone numbers and citizen IDs.
- Keep one clean demo flow from owner to report dashboard.
- Before presenting, run `python manage.py check`.
