# Basic Guide for New Users and Miners (Issue #47)

This guide is a minimal onboarding path for running and understanding this project.

## 1) What this project currently does
- Implements a small blockchain model for learning/testing.
- Includes proof-of-work and chain validation primitives.
- Includes a demo script that mines blocks and validates the result.

## 2) Prerequisites
- Install [Bun](https://bun.sh/)
- Clone the repository

```bash
git clone git@github.com:LennyMalcolm0/bitcoin.git
cd bitcoin
```

## 3) Run the demo

```bash
bun run blockchain-demo.ts
```

Expected behavior:
- The script mines blocks.
- It prints whether chain validation succeeds.

## 4) Miner quick checklist
- Ensure your machine clock is correct.
- Keep difficulty and nonce rules unchanged while testing.
- Validate every new block before appending.

## 5) New contributor workflow
1. Create a branch for one scoped change.
2. Keep PR small and testable.
3. Include a short runbook in PR description.

## 6) Next learning steps
- Add transaction data into mined blocks.
- Add mempool handling.
- Add chain persistence and restart recovery.

## 7) Reviewer-friendly verification checklist
Use this checklist when reviewing PRs for this guide:
- Fresh clone + install succeeds.
- Demo command runs without manual file edits.
- Guide sections match actual command/file names.
- "Expected behavior" output stays accurate after recent changes.

Quick verify:
```bash
bun install
bun run blockchain-demo.ts
```

## 8) Common troubleshooting
- `bun: command not found`: install Bun and restart terminal.
- Demo output differs: pull latest `main`, then rerun install + demo.
- Local edits break flow: stash/reset local changes before retrying.
