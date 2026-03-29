# Bitcoin P2P Electronic Cash System

A Python + TypeScript implementation of a Bitcoin-like peer-to-peer electronic cash system. Supports blockchain operations, wallet management, P2P networking simulation, and network metrics.

## Architecture

The system is composed of four core components:

| Component | File | Description |
|-----------|------|-------------|
| **Blockchain** | `Bitcoin-Client-Architecture.py` | Storage, consensus, and transaction validation |
| **Wallet** | `Bitcoin-Client-Architecture.py` | Key generation, balance management, transaction signing |
| **P2P Network** | `Bitcoin-Client-Architecture.py` | Peer discovery and network communication |
| **Metrics** | `metric-engine.py` | Network statistics and dashboard |

## Installation

```bash
pip install hashlib time json  # Standard library only
python Bitcoin-Client-Architecture.py
```

## Quick Start

```python
from Bitcoin_Client_Architecture import BitcoinCore

client = BitcoinCore()
client.start()
```

## API Reference

See [docs/API.md](docs/API.md) for full API documentation.

## License

MIT
