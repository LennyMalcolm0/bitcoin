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
