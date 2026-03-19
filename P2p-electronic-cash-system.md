# P2P Electronic Cash System — Concept Document
**Issue #5 · $300 Bounty**

---

## Overview

A peer-to-peer electronic cash system enables two parties to transact directly with each other over the internet — no bank, payment processor, or any trusted third party required. The core problem it solves is **trust**: how do you stop someone from spending the same money twice without a central authority keeping score?

---

## Core Problems to Solve

### 1. Double Spending
In a physical cash system, handing over a bill makes it gone. Digitally, a file can be copied. The system must ensure that once a unit of value is sent, the sender can no longer spend it.

### 2. Trust Without Intermediaries
Banks work because we trust them. A P2P system replaces institutional trust with **cryptographic proof** — math that anyone can verify independently.

### 3. Transaction Ordering
Without a central ledger, the network must agree on which transaction happened first. This is the **consensus problem**.

---

## System Architecture

### Transactions
Each transaction is a digitally signed message of the form:

```
{
  sender_public_key,
  recipient_public_key,
  amount,
  reference_to_previous_transaction,
  signature (signed with sender's private key)
}
```

Ownership is proved by signature. Anyone can verify the sender owns the funds without needing to know who they are.

### The Ledger (Blockchain)
Transactions are batched into **blocks**. Each block:
- Contains a set of valid transactions
- References the hash of the previous block (forming a chain)
- Includes a proof-of-work stamp (see below)

This creates an append-only, tamper-evident history. Altering any past block invalidates every block after it.

### Proof of Work
To add a block, a node must solve a computational puzzle — finding a number (`nonce`) such that the block's hash starts with N zeroes. This:
- Makes block creation costly
- Makes rewriting history exponentially costly
- Determines who gets to add the next block (first to solve wins)

### The Network
- Any node can join or leave freely
- New transactions are broadcast to all nodes
- Nodes always extend the **longest valid chain**
- Consensus is emergent — no coordinator needed

---

## Transaction Lifecycle

```
1. Alice wants to send 10 coins to Bob
         |
2. Alice signs a transaction with her private key
         |
3. Transaction is broadcast to the peer network
         |
4. Nodes validate: Does Alice have the funds? Is the signature valid?
         |
5. Transaction sits in the mempool (pending pool)
         |
6. A miner batches it into a block and solves proof-of-work
         |
7. Block is broadcast — other nodes verify and accept it
         |
8. Bob's balance is updated in the new chain state
```

---

## Key Properties

| Property | How It's Achieved |
|---|---|
| No intermediary | Direct node-to-node broadcast |
| Tamper resistance | Hash chaining + proof of work |
| Double-spend prevention | Longest chain consensus |
| Pseudonymity | Public key addresses, not names |
| Openness | Anyone can run a node |
| Finality | Grows stronger with each additional block |

---

## Handling Edge Cases

### Forks
Two miners may solve a block simultaneously, creating a temporary fork. Nodes follow the longest chain; the shorter branch is discarded and its transactions return to the mempool.

### Incentives
Miners are rewarded with:
1. **Block reward** — newly minted coins for finding a block
2. **Transaction fees** — small amounts attached by senders

This aligns miner incentives with honest participation.

### Lost Keys
Private key loss means permanent loss of funds. The system has no password reset — this is a deliberate trade-off for censorship resistance.

---

## What This System Is NOT

- **Not anonymous** — all transactions are public; addresses are pseudonymous
- **Not instant** — confirmation takes time (one block ≈ minutes)
- **Not free** — transaction fees exist to prioritize inclusion
- **Not scalable infinitely** — block size and frequency create throughput limits

---

## Implementation Considerations

- **Key management**: Wallet software handles key generation, storage, signing
- **Node discovery**: DNS seeds or hardcoded bootstrap peers for initial connection
- **Merkle trees**: Transactions within a block are hashed into a Merkle tree for efficient verification
- **SPV clients**: Lightweight clients verify their own transactions without downloading the full chain

---

## Summary

The system replaces the trusted third party with a distributed network of self-interested validators. Trust is not eliminated — it is redistributed from a single institution to a mathematical protocol that anyone can audit and anyone can run. The result is a payment system that is open, borderless, and resistant to censorship or single points of failure.
