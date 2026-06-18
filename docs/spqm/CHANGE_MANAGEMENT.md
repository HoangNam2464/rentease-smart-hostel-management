# RentEase Change Management

## Change Principles

RentEase changes should be small, phase-based, and easy to review.

Use the `complete-product` branch unless explicitly approved otherwise.

Do not run `git pull`, merge branches, or switch branches without explicit approval.

Do not touch `temp-auto-auth-bypass`.

## Change Scope

Each change should define:

- phase name
- goal
- allowed files
- forbidden files
- migration impact
- route or feature verification
- security/privacy verification
- expected commit message

## Schema And Migration Control

Do not change models or schema without explicit approval.

Do not create migrations unless explicitly approved.

If a task unexpectedly requires schema changes, stop and report before implementing.

## Commit Rules

Use short, phase-specific commit messages.

Examples:

- `Remove legacy API and fees root routes`
- `Add RentEase agent guidance docs`
- `Polish public landing page`

Before committing:

```powershell
git status --short
```

Only intended files should be modified or staged.

## Tag Rules

Use tags for locked milestones.

Do not create a tag until final verification and explicit approval.

Do not force push tags.

Do not move existing tags unless explicitly approved.

## Review Style

For a two-person or course project, direct review in the working branch may be enough.

If more collaborators join later, pull request/review style can be used for:

- production settings
- authentication/account lifecycle
- billing changes
- security hardening
- deployment changes

## Forbidden Change Patterns

Do not:

- force push
- reset hard
- restore all files
- delete legacy apps without approval
- rename `hostello_backend`
- re-add root legacy routes
- commit secrets, `.env`, database files, or backup dumps
- alter owner/tenant scoping casually
