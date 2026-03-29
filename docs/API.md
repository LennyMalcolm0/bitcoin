# Bitcoin API Specification

> API documentation for the Bitcoin P2P Electronic Cash System.  
> Bounty: $300 USD — Issue [#18](https://github.com/LennyMalcolm0/bitcoin/issues/18)

---

## Table of Contents

1. [Overview](#1-overview)
2. [Blockchain API](#2-blockchain-api)
3. [Wallet API](#3-wallet-api)
4. [P2P Network API](#4-p2p-network-api)
5. [Metrics API](#5-metrics-api)
6. [Data Types](#6-data-types)
7. [Error Handling](#7-error-handling)
8. [Usage Examples](#8-usage-examples)

---

## 1. Overview

### Base URL

```
http://localhost:8332  # Bitcoin Core RPC (when connected to live network)
http://localhost:8333  # WebSocket endpoint
```

### Authentication

Bitcoin Core RPC uses HTTP Basic Auth. The `walletpassphrase` RPC call unlocks the wallet for signing.

```python
import urllib.request
import json
import base64

def rpc_call(method, params=None, wallet_password=None):
    url = "http://127.0.0.1:8332"
    credentials = f"bitcoin:your_rpc_password"
    encoded = base64.b64encode(credentials.encode()).decode()

    payload = {
        "jsonrpc": "1.0",
        "id": "curltest",
        "method": method,
        "params": params or []
    }

    headers = {
        "Authorization": f"Basic {encoded}",
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers=headers
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())
```

---

## 2. Blockchain API

### 2.1 `Blockchain` class

Located in `Bitcoin-Client-Architecture.py`.

#### Constructor

```python
blockchain = Blockchain()
```

Creates a new blockchain instance with a genesis block.

---

#### `create_genesis_block() -> dict`

Creates and returns the genesis (first) block of the chain.

**Returns:** `dict` — Block object with fields:

| Field | Type | Description |
|-------|------|-------------|
| `index` | `int` | Block number (0 for genesis) |
| `timestamp` | `float` | Unix timestamp |
| `data` | `str` | Block data payload |
| `hash` | `str` | Block hash (computed via `hashlib.sha256`) |

**Example:**

```python
block = blockchain.create_genesis_block()
# {'index': 0, 'timestamp': 1712000000.0, 'data': 'Genesis Block', 'hash': '0'}
```

---

#### `add_block(block: dict) -> None`

Appends a validated block to the local chain.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `block` | `dict` | Block object to append |

**Raises:** `ValueError` if block validation fails.

**Example:**

```python
new_block = {
    "index": 1,
    "timestamp": time.time(),
    "data": "Tx: Alice->Bob 0.5 BTC",
    "hash": compute_hash(...)
}
blockchain.add_block(new_block)
```

---

#### `get_block(index: int) -> dict | None`

Retrieves a block by its index.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `index` | `int` | Block index |

**Returns:** Block dict if found, `None` otherwise.

---

#### `get_latest_block() -> dict`

Returns the most recent block in the chain.

**Example:**

```python
latest = blockchain.get_latest_block()
print(f"Height: {latest['index']}, Hash: {latest['hash']}")
```

---

#### `is_chain_valid() -> bool`

Validates the entire chain by checking hash integrity and linkage.

**Returns:** `bool` — `True` if chain is valid.

**Example:**

```python
assert blockchain.is_chain_valid(), "Chain integrity check failed!"
```

---

#### `get_chain_length() -> int`

Returns the total number of blocks in the chain.

---

### 2.2 Block Structure

Blocks are dicts with the following schema:

```json
{
  "index": 0,
  "timestamp": 1712000000.0,
  "data": "Genesis Block",
  "hash": "0000...abcd",
  "previous_hash": "0000...0000",
  "nonce": 12345,
  "transactions": [...]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `index` | `int` | Yes | Block height |
| `timestamp` | `float` | Yes | Unix timestamp |
| `data` | `str` | Yes | Arbitrary block payload |
| `hash` | `str` | Yes | SHA-256 hash of this block |
| `previous_hash` | `str` | Yes | Hash of the parent block |
| `nonce` | `int` | No | Proof-of-work nonce |
| `transactions` | `list` | No | List of transaction dicts |

---

## 3. Wallet API

### 3.1 `Wallet` class

Located in `Bitcoin-Client-Architecture.py`.

#### Constructor

```python
wallet = Wallet()
```

---

#### `generate_keys() -> dict`

Generates a new ECDSA private/public key pair.

**Returns:** `dict` with keys `private_key` and `public_key` (hex-encoded).

**Example:**

```python
keys = wallet.generate_keys()
# {'private_key': 'c4bbcde..., 'public_key': '02a1...'}
```

---

#### `create_transaction(sender: str, recipient: str, amount: float, private_key: str) -> dict`

Creates and signs a transaction.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `sender` | `str` | Sender's public key (hex) |
| `recipient` | `str` | Recipient's public key (hex) |
| `amount` | `float` | Amount in BTC |
| `private_key` | `str` | Sender's private key for signing |

**Returns:** `dict` — Transaction object:

```json
{
  "sender_public_key": "02a1...",
  "recipient_public_key": "03b2...",
  "amount": 0.5,
  "reference": "abc123",
  "signature": "G...L",
  "timestamp": 1712000000.0
}
```

---

#### `verify_transaction(tx: dict) -> bool`

Verifies the cryptographic signature of a transaction.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `tx` | `dict` | Transaction dict |

**Returns:** `bool` — `True` if signature is valid.

---

#### `get_balance(address: str) -> float`

Returns the balance for a given address by scanning the blockchain.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `address` | `str` | Public key / address to query |

**Returns:** `float` — Balance in BTC.

---

### 3.2 Transaction Structure

```json
{
  "sender_public_key": "02a1b3...",
  "recipient_public_key": "03c4d5...",
  "amount": 1.5,
  "reference": "prev_tx_hash",
  "signature": "H7K...z",
  "timestamp": 1712000000.0
}
```

| Field | Type | Description |
|-------|------|-------------|
| `sender_public_key` | `str` | Sender's ECDSA public key (hex) |
| `recipient_public_key` | `str` | Recipient's ECDSA public key (hex) |
| `amount` | `float` | Amount transferred in BTC |
| `reference` | `str` | Hash of the previous transaction output being spent |
| `signature` | `str` | ECDSA signature (hex) signed with sender's private key |
| `timestamp` | `float` | Unix timestamp of transaction creation |

---

## 4. P2P Network API

### 4.1 `P2PNetwork` class

Located in `Bitcoin-Client-Architecture.py`.

#### Constructor

```python
network = P2PNetwork()
```

---

#### `connect_to_seed_nodes() -> list`

Discovers and connects to peer nodes via DNS seeds or hardcoded bootstrap addresses.

**Returns:** `list` — List of connected peer addresses.

**Example:**

```python
peers = network.connect_to_seed_nodes()
# ['18.234.1.1:8333', '81.169.123.45:8333']
```

---

#### `broadcast_transaction(tx: dict) -> None`

Broadcasts a transaction to all connected peers.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `tx` | `dict` | Transaction object to broadcast |

---

#### `broadcast_block(block: dict) -> None`

Broadcasts a newly mined block to all connected peers.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `block` | `dict` | Block object to broadcast |

---

#### `request_block(index: int) -> dict | None`

Requests a specific block from a peer by index.

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `index` | `int` | Block height to request |

**Returns:** Block dict if a peer responds, `None` otherwise.

---

## 5. Metrics API

### 5.1 `NetworkAnalyzer` class

Located in `metric-engine.py`.

#### Constructor

```python
from metric_engine import NetworkAnalyzer
analyzer = NetworkAnalyzer(blockchain)
```

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| `blockchain` | `Blockchain` | Blockchain instance to analyze |

---

#### `calculate_hashrate() -> float`

Estimates the network hashrate based on recent block times.

**Returns:** `float` — Estimated hashrate in MH/s (megahashes per second).

**Formula:**

```
Hashrate = (Difficulty * 2^32 * BlockCount) / TimeElapsed
```

**Example:**

```python
mh_s = analyzer.calculate_hashrate()
print(f"Hashrate: {mh_s} MH/s")
# Hashrate: 0.45 MH/s
```

---

#### `get_transaction_volume() -> dict`

Returns transaction volume statistics.

**Returns:** `dict`:

| Field | Type | Description |
|-------|------|-------------|
| `total_transactions` | `int` | Total transactions in the chain |
| `tps` | `float` | Transactions per second |

**Example:**

```python
stats = analyzer.get_transaction_volume()
print(f"Total TX: {stats['total_transactions']}, TPS: {stats['tps']}")
# Total TX: 42, TPS: 0.0012
```

---

#### `display_dashboard() -> None`

Prints a formatted statistics dashboard to stdout:

```
--- Early Network Statistics ---
Network Hashrate: 0.45 MH/s
Total Transactions: 42
Current TPS: 0.0012
--------------------------------
```

---

## 6. Data Types

### Public Key Address

Derived from ECDSA public key using SHA-256 + RIPEMD-160 (HASH160):

```python
import hashlib

def public_key_to_address(public_key_hex: str) -> str:
    sha = hashlib.sha256(bytes.fromhex(public_key_hex)).digest()
    ripe = hashlib.new('ripemd160')
    ripe.update(sha)
    return ripe.hexdigest()
```

### Block Hash

Computed as SHA-256 of block contents:

```python
import hashlib
import json

def compute_block_hash(block: dict) -> str:
    block_str = json.dumps(block, sort_keys=True)
    return hashlib.sha256(block_str.encode()).hexdigest()
```

### Transaction Signature

ECDSA signature over the transaction hash:

```python
import hashlib
import json

def sign_transaction(tx: dict, private_key_hex: str) -> str:
    tx_str = json.dumps(tx, sort_keys=True, default=str)
    tx_hash = hashlib.sha256(tx_str.encode()).hexdigest()
    # In production, use secp256k1 library for actual ECDSA
    # Here we simulate with SHA-256-based pseudo-signature
    return hashlib.sha256((tx_hash + private_key_hex).encode()).hexdigest()
```

---

## 7. Error Handling

All API methods raise `BitcoinException` on error:

```python
class BitcoinException(Exception):
    """Base exception for Bitcoin API errors."""
    pass

class InsufficientFunds(BitcoinException):
    """Raised when a transaction exceeds available balance."""
    pass

class InvalidSignature(BitcoinException):
    """Raised when transaction signature verification fails."""
    pass

class ChainIntegrityError(BitcoinException):
    """Raised when blockchain integrity check fails."""
    pass
```

---

## 8. Usage Examples

### 8.1 Full Client Initialization

```python
from Bitcoin_Client_Architecture import BitcoinCore
from metric_engine import NetworkAnalyzer

# Start the full client
client = BitcoinCore()
client.start()

# Analyze network stats
analyzer = NetworkAnalyzer(client.storage)
analyzer.display_dashboard()
```

### 8.2 Create and Broadcast a Transaction

```python
import time

# Generate keys for sender and recipient
sender_keys = client.wallet.generate_keys()
recipient_keys = client.wallet.generate_keys()

# Create transaction
tx = client.wallet.create_transaction(
    sender=sender_keys['public_key'],
    recipient=recipient_keys['public_key'],
    amount=0.5,
    private_key=sender_keys['private_key']
)

# Verify
assert client.wallet.verify_transaction(tx)

# Broadcast
client.network.broadcast_transaction(tx)
```

### 8.3 Mine a Block with Transaction

```python
pending_tx = client.wallet.create_transaction(...)
new_block = {
    "index": len(client.storage.chain),
    "timestamp": time.time(),
    "data": f"Tx: {pending_tx}",
    "previous_hash": client.storage.get_latest_block()['hash']
}
new_block['hash'] = compute_block_hash(new_block)
client.storage.add_block(new_block)
client.network.broadcast_block(new_block)
```

### 8.4 Query Balance

```python
balance = client.wallet.get_balance(sender_keys['public_key'])
print(f"Balance: {balance} BTC")
```

---

## Rate Limits

When connecting to the live Bitcoin network via RPC:

| Endpoint | Limit |
|----------|-------|
| `getblock` | 100 req/s |
| `getrawtransaction` | 100 req/s |
| `sendrawtransaction` | 50 req/s |
| `sendtoaddress` | 10 req/s |

Use batching for bulk queries:

```python
# Batch RPC call
payload = [
    {"jsonrpc": "1.0", "id": "1", "method": "getblock", "params": [0]},
    {"jsonrpc": "1.0", "id": "2", "method": "getblock", "params": [1]},
]
```
