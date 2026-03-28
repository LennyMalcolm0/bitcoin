# Not a real project
# Used for testing

## Bounty #23 Progress (Block Creation + Validation)

Added a minimal, reviewable block lifecycle implementation:

- `blockchain.ts`
  - `mineBlock(...)`
  - `validateBlock(...)`
  - `validateChain(...)`
- `blockchain-demo.ts`
  - mines two connected blocks and validates the chain

### Quick run

```bash
bun run blockchain-demo.ts
```

This is the first reviewable slice before adding networking/mempool rules.
