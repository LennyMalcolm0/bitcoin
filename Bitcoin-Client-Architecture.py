"""
Bitcoin Client Architecture — Core component assembly.

This module provides the BitcoinCore class that assembles all components
(Blockchain, Wallet, P2P Network) into a working client.
For the full API documentation, see docs/API.md and the api/ module.
"""

import hashlib
import time
import json
import sys
from pathlib import Path

# Import from the api/ module if available, fall back to inline classes
sys.path.insert(0, str(Path(__file__).parent))
try:
    from api import Blockchain, Wallet, P2PNetwork, NetworkAnalyzer
    from api import BitcoinException, compute_block_hash
    HAS_API_MODULE = True
except ImportError:
    HAS_API_MODULE = False


class BitcoinComponent:
    """Base class for Bitcoin Core components."""
    def __init__(self, name: str):
        self.name = name
        print(f"[{self.name}] Initialized.")


if not HAS_API_MODULE:
    # Minimal fallback implementations if api/ module is not available

    def compute_block_hash(block: dict) -> str:
        """Fallback block hash computation."""
        fields = {k: v for k, v in block.items() if k != 'hash'}
        return hashlib.sha256(
            json.dumps(fields, sort_keys=True, default=str).encode()
        ).hexdigest()

    class Blockchain(BitcoinComponent):
        def __init__(self):
            super().__init__("Storage & Consensus")
            self.chain = [self.create_genesis_block()]
            self.pending_transactions = []

        def create_genesis_block(self):
            return {
                "index": 0,
                "timestamp": time.time(),
                "data": "Genesis Block",
                "hash": "0",
                "previous_hash": "0",
                "transactions": []
            }

        def add_block(self, block):
            self.chain.append(block)
            print(f"[{self.name}] New block added to the local ledger.")

        def get_latest_block(self):
            return self.chain[-1]

        def is_chain_valid(self):
            return True

    class P2PNetwork(BitcoinComponent):
        def __init__(self):
            super().__init__("Networking")
            self.peers = []

        def connect_to_seed_nodes(self):
            print(f"[{self.name}] Connecting to Bitcoin network peers...")

    class Wallet(BitcoinComponent):
        def __init__(self):
            super().__init__("Wallet")
            self.balance = 0.0

        def generate_keys(self):
            print(f"[{self.name}] Generating ECDSA private/public key pair...")


class BitcoinCore:
    """
    Bitcoin Core Client — assembles all components into a working node.

    Attributes:
        storage: Blockchain component for ledger operations.
        network: P2P Network component for peer communication.
        wallet: Wallet component for key management and transactions.
        analyzer: NetworkAnalyzer for metrics (if api module available).

    Example::

        client = BitcoinCore()
        client.start()
        keys = client.wallet.generate_keys()
        tx = client.wallet.create_transaction(keys['public_key'], recipient, 0.5, keys['private_key'])
        client.network.broadcast_transaction(tx)
    """

    def __init__(self):
        print("--- Starting Bitcoin Core Client ---")
        self.storage = Blockchain()
        self.network = P2PNetwork()
        self.wallet = Wallet()

        if HAS_API_MODULE:
            self.analyzer = NetworkAnalyzer(self.storage)
        else:
            self.analyzer = None

    def start(self):
        """
        Initialize and start the Bitcoin Core client.

        Synchronizes with the network, generates initial keys,
        and processes any pending blocks.
        """
        print("\n[System] Synchronizing with network...")
        self.network.connect_to_seed_nodes()
        self.wallet.generate_keys()

        # Process pending transactions from last shutdown
        pending = self.storage.get_pending_transactions() if hasattr(self.storage, 'get_pending_transactions') else []

        # Create a simulated first block
        latest = self.storage.get_latest_block()
        mock_block = {
            "index": latest['index'] + 1,
            "timestamp": time.time(),
            "data": f"System startup — {len(pending)} pending transactions",
            "previous_hash": latest.get('hash', compute_block_hash(latest)),
            "transactions": pending
        }
        mock_block['hash'] = compute_block_hash(mock_block)
        self.storage.add_block(mock_block)

        print("\n[System] Bitcoin Core is running and synchronized.")

        if self.analyzer:
            self.analyzer.display_dashboard()

    def get_status(self) -> dict:
        """
        Return the current client status.

        Returns:
            dict with keys: chain_length, peer_count, latest_hash.
        """
        return {
            "chain_length": len(self.storage.chain),
            "peer_count": self.network.get_peer_count() if hasattr(self.network, 'get_peer_count') else 0,
            "latest_hash": self.storage.get_latest_block().get('hash', 'N/A'),
            "timestamp": time.time()
        }


# --- Entry Point ---

if __name__ == "__main__":
    client = BitcoinCore()
    client.start()

    # Run a quick demo
    print("\n--- Quick Demo ---")
    keys = client.wallet.generate_keys()
    print(f"Public key: {keys.get('public_key', 'N/A')[:16]}...")
    status = client.get_status()
    print(f"Chain length: {status['chain_length']}, Peers: {status['peer_count']}")
    print("\nClient demo complete.")
