# RentEase Security Notes

## Repository Safety

- Do not commit `.env`.
- Do not commit `db.sqlite3` for public repositories.
- Do not commit `backup_phase*.json`.
- Do not use real user data in demo records.
- Do not publish real phone numbers, citizen IDs, emails, or payment data.

## Backup Files

Database dumps can contain:

- password hashes
- admin usernames
- email addresses
- phone numbers
- citizen IDs
- tenant or payment records

Keep backup files local unless the repository is private and sharing is controlled.

## Credentials

Use environment variables for:

- `SECRET_KEY`
- email username/password
- payment provider keys

The development fallback secret key is only for local demo use.

## Password Rotation

If backup JSON files were ever exposed publicly, rotate demo/admin passwords before submission or presentation.

## Demo Data

Use fake data only:

- fake names
- fake phone numbers
- fake emails
- fake citizen IDs
- fake payment transaction codes
