# Not a real project
# Used for testing

## Bounty #22 Progress (Proof-of-Work)

Added a minimal, reviewable PoW implementation:

- `pow.ts`
  - `calculatePowHash(...)`
  - `isValidPow(...)`
  - `mineProofOfWork(...)`
- `pow-demo.ts`
  - runnable example that mines a block with configurable difficulty

### Quick run

```bash
bun run pow-demo.ts
```

This is an incremental slice meant for review before wiring into a full blockchain loop.
