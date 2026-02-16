# Next-Phase Development Plan (Issue #50)

This document proposes a minimal roadmap for the next phase after validating the basic blockchain flow.

## Current Baseline
- Basic blockchain structure exists.
- Proof-of-work and block validation skeleton are in place.
- A demo path can mine and validate a tiny chain.

## Goals for Phase 2
1. **Transaction Pipeline**
- Add a transaction model with basic shape validation.
- Add transaction inclusion rules for mined blocks.

2. **Mempool + Miner Loop**
- Add an in-memory mempool with deduplication.
- Add a miner loop that consumes mempool transactions.

3. **Consensus Safety Checks**
- Enforce previous-hash continuity and difficulty checks in one validation path.
- Add explicit rejection reasons for invalid chains and blocks.

4. **Persistence + Recoverability**
- Persist chain state to local storage.
- Add restart/reload flow for development testing.

## Milestones
- **M1 (small PR):** Transaction model + tests
- **M2 (small PR):** Mempool integration + miner flow
- **M3 (small PR):** Validation hardening + detailed errors
- **M4 (small PR):** Persistence + startup recovery

## Acceptance Criteria
- `bun run blockchain-demo.ts` still works.
- Each milestone ships with at least one runnable validation/demo step.
- Clear README pointers for running and verifying each milestone.

## Review Package (for bounty evaluation)
To reduce review turnaround, the implementation should be submitted as four small PRs that map 1:1 to milestones.

Per PR, include:
- Scope statement (what is in/out for the milestone)
- Repro steps (`bun install` then the exact run command)
- Expected output snapshot (short terminal output snippet)
- Risks and rollback note (how to revert safely if behavior regresses)

### Suggested validation commands
```bash
bun install
bun run blockchain-demo.ts
```

For milestone PRs that add tests, also run:
```bash
bun test
```
