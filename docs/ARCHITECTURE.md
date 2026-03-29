# Bitcoin Client Architecture

> System architecture documentation for the Bitcoin P2P Electronic Cash System.

## System Overview

The system implements a simplified Bitcoin-like blockchain with four core components:

```
┌──────────────────────────────────────────────┐
│              BitcoinCore (Main)              │
├──────────────┬──────────────┬────────────────┤
│  Blockchain  │    Wallet    │  P2P Network    │
│  (Storage)   │  (Keys/Tx)   │  (Comms)       │
├──────────────┴──────────────┴────────────────┤
│           NetworkAnalyzer (Metrics)          │
└──────────────────────────────────────────────┘
```

## Component Details

### 1. Blockchain (`Bitcoin-Client-Architecture.py`)

Responsible for storage, consensus, and transaction validation.

**Key operations:**
- Genesis block creation
- Block validation and appending
- Chain integrity verification (hash chain)
- Double-spending prevention via longest-chain rule

**Data model:**
- Chain: `list[dict]` — ordered list of blocks
- Each block: `{index, timestamp, data, hash, previous_hash, nonce, transactions}`

### 2. Wallet (`Bitcoin-Client-Architecture.py`)

Handles cryptographic key management and transaction signing.

**Key operations:**
- ECDSA key pair generation
- Transaction creation and signing
- Signature verification
- Balance computation from blockchain

**Key derivation:**
- Private key: 256-bit random integer
- Public key: ECDSA point multiplication on secp256k1 curve
- Address: HASH160(public_key)

### 3. P2P Network (`Bitcoin-Client-Architecture.py`)

Simulates peer-to-peer networking layer.

**Key operations:**
- Seed node discovery
- Transaction broadcast
- Block broadcast
- Block requests by index

### 4. NetworkAnalyzer (`metric-engine.py`)

Provides network statistics and monitoring.

**Metrics:**
- Estimated network hashrate (MH/s)
- Transaction throughput (TPS)
- Chain length and growth rate

## Security Model

| Threat | Mitigation |
|--------|------------|
| Double spending | Longest-chain consensus; transaction references |
| Tampering | SHA-256 hash chain linkage |
| Key theft | Private keys never transmitted over network |
| Sybil attacks | Proof-of-work makes block creation expensive |

## Extension Points

- Replace mock PoW with actual difficulty adjustment (DAA)
- Add SPV (Simplified Payment Verification) client
- Implement Merkle tree for transaction verification
- Add BIP-32 HD wallet support
- Integrate with Bitcoin Core via RPC for testnet/mainnet
