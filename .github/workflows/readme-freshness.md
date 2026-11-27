---
description: Audit README freshness against changes on main
on:
  push:
    branches:
      - main
  schedule:
    - cron: "0 18 * * *"
      timezone: "Asia/Kolkata"
  workflow_dispatch:
permissions:
  contents: read
  issues: read
  copilot-requests: write
imports:
  - .github/agents/readme-freshness-auditor.agent.md
safe-outputs:
  create-issue:
    title-prefix: "[README freshness] "
    max: 1
checkout: false
tools:
  bash: false
  cli-proxy: false
  edit: false
  github:
    toolsets:
      - repos
      - issues
    allowed:
      - get_commit
      - get_file_contents
      - list_commits
      - list_issues
jobs:
  agent:
    permissions:
      contents: read
      issues: read
      copilot-requests: write
---

# README Freshness Audit

Use the imported README Freshness Auditor instructions.

## Run context

- Event: `${{ github.event_name }}`
- Repository: `${{ github.repository }}`
- Push range start (empty for non-push events): `${{ github.event.before }}`
- Push range end: `${{ github.event.after }}`

For push events, audit the full supplied range. For scheduled and manually dispatched events, resolve the latest commit on `main` and audit its history back to the latest earlier commit that changed the root README, as described by the agent. Create an issue only for a verified, material README gap that does not already have an open issue.
