# Python/Django Quality Stack

## Purpose

This file maps generic SPQM or course quality requirements to Python/Django equivalents for RentEase.

RentEase is a Python/Django project. Do not add Node.js, Express, Jest, or ESLint just to satisfy generic quality wording.

## Technology Mapping

| Generic Requirement | RentEase Python/Django Equivalent | Current Status |
| --- | --- | --- |
| Node.js + Express | Django | Already used |
| REST route testing with Supertest | Django test client or pytest-django | Planned |
| Jest tests | Django `TestCase` or pytest | Planned |
| ESLint | ruff or flake8 | Planned |
| Prettier | black for Python formatting, djlint for templates if adopted | Planned |
| npm scripts | Python/Django management commands or shell scripts | Planned |
| GitHub Actions | Python/Django CI workflow | Planned |
| SonarQube | Optional code quality scanning | Planned |
| Docker Compose | Optional Django app + database deployment setup | Planned |
| PostgreSQL | Production database target | Planned |
| Redis | Optional cache/session/task support later | Planned |
| Prometheus/Grafana | Optional monitoring later | Planned |

## Current Quality Commands

Use direct venv Python:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py makemigrations --check --dry-run
```

Do not use global `python` unless the environment is explicitly fixed.

## Recommended Future Quality Stack

Near-term:

- Django `TestCase` tests for permissions and critical workflows
- Django test client for route regression
- ruff or flake8 for linting
- black for formatting
- GitHub Actions for check, migrations dry-run, and tests

Medium-term:

- coverage reporting
- pytest-django if the team prefers pytest
- deployment checks
- production settings validation

Later:

- SonarQube or similar quality scanning
- Docker Compose for app + database
- PostgreSQL for production
- Redis if caching or async jobs are added
- monitoring and alerting

## Adoption Rule

Treat these tools as future quality improvements, not immediate implementation.

Do not add a new tool without:

- a clear phase plan
- approval
- local verification
- documentation update
- CI/update plan if relevant
