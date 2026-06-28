# RentEase Design Workflows

Load only the workflow that matches the requested mode.

## Shape

Do not edit. Produce a compact design brief containing:

- target user and job
- current friction supported by source or rendered evidence
- content and action hierarchy
- reuse of existing tokens and components
- loading, empty, error, permission, and success states
- desktop and mobile behavior
- intended files and verification

Call out any required backend or data change as a separate dependency; do not hide it inside UI work.

## Craft

Shape first, then implement the smallest complete vertical slice. Preserve Django template tags, URLs, form behavior, CSRF handling, role scoping, and accessible semantics. Finish with browser verification and repository checks.

## Critique

Do not edit. Inspect both source and rendered output when available. Report findings by severity with concrete evidence and user impact. Cover hierarchy, clarity, action priority, density, consistency, trust, and role suitability. End with the three highest-value improvements.

## Audit

Do not edit unless the user also asks for fixes. Check:

- semantic headings, labels, keyboard flow, visible focus, and contrast
- desktop/mobile layout, overflow, tables, and touch targets
- loading, empty, error, validation, success, and permission states
- natural Vietnamese copy and long-content resilience
- design-token and component reuse
- broken assets or raw Django template syntax
- public/owner/tenant/staff data exposure and role boundaries

Separate observed failures from unverified risks.

## Polish

Implement focused refinements without changing the surface's product behavior. Fix inconsistent spacing, hierarchy, alignment, typography, controls, statuses, and responsive details. Avoid broad redesign when a local correction solves the problem.

## Adapt

Test the actual content at desktop and mobile sizes. Prefer fluid layout, wrapping, and horizontal table scrolling before adding breakpoints. Preserve action reachability, reading order, and useful information on small screens.

## Harden

Handle realistic operational states: no data, partial data, long names, large currency values, overdue statuses, validation errors, unavailable actions, slow/loading feedback, and denied access. Never invent private fallback data to fill a UI.

## Clarify

Use concise Vietnamese-first copy. Prefer direct verbs and domain terms used elsewhere in RentEase. Labels must explain the data requested; errors must state what happened and what the user can do next. Do not expose credentials, implementation details, or internal permission language.

## Verification Evidence

Record what was actually checked: route, role, viewport, interaction, and command result. Do not turn old screenshots or historical phase results into current proof.
