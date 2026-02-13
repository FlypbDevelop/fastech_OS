---
name: web-design-guidelines
description: Audit UI code for accessibility, performance, and adherence to Vercel's Web Interface Guidelines. Use when asked to "review my UI", "check accessibility", "audit design", or "review UX".
license: MIT
compatibility: Requires network access to fetch live guidelines and file read permissions.
metadata:
  author: vercel
  version: 1.0.0
---

# Web Interface Guidelines

This skill audits your project's UI code against the official Vercel Web Interface Guidelines. It is designed to be used **after** coding, acting as an automated linter for design and accessibility best practices.

## Workflow Integration
This skill is part of a standard design workflow:
1.  **DESIGN** → Learn principles (Use `frontend-design` skill)
2.  **CODE** → Implement the interface
3.  **AUDIT** → **Run this `web-design-guidelines` skill**
4.  **FIX** → Address the reported findings

## Audit Process

When activated, this skill follows these steps:

1.  **Fetch Guidelines**: Retrieves the latest rule set from the official source:
    `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`
2.  **Target Selection**:
    -   If the user provides specific files or a glob pattern (e.g., `src/components/*.tsx`), the skill audits only those targets.
    -   If no targets are provided, the skill prompts the user: "Which files or patterns should I review?"
3.  **Analysis**: Applies all rules from the fetched guidelines against the content of the specified files.
4.  **Reporting**: Outputs all findings strictly using the **terse `file:line` format** specified in the guidelines document.

## Input Parameters

This skill accepts an optional file path or glob pattern as an argument.

**Example usage in user request:**
> "Review my UI in `app/page.tsx` and `components/button.tsx`"
> "Check accessibility for `src/**/*.vue`"

## Related Resources

For detailed rule explanations and advanced troubleshooting, refer to the following files bundled with this skill:

-   **Reference Docs**: See the [`/references/`](./references/) folder for deep dives on specific guidelines (e.g., color contrast, semantic HTML).
-   **Templates**: See the [`/assets/`](./assets/) folder for accessible component templates and pattern examples.
