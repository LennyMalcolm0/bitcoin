#!/usr/bin/env python3
"""
Bitcoin API Usage Examples

Demonstrates all major API endpoints and patterns.
Run with: python3 examples/demo.py
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for api module
sys.path.insert(0, str(Path(__file__).parent.parent))

from api import (
    Wallet, Blockchain, P2PNetwork, NetworkAnalyzer,
    BitcoinException, compute_block_hash
)


def demo_blockchain():
    """Demonstrate Blockchain API."""
    print("\n=== Blockchain API Demo ===")
    bc = Blockchain()

    # Create and add blocks
    for i in range(1, 4):
        prev = bc.get_latest_block()
        block = {
            "index": i,
            "timestamp": time.time(),
            "data": f"Block {i} data",
            "previous_hash": prev.get('hash', compute_block_hash(prev)),
            "transactions": [{"tx": f"tx_{i}"}]
        }
        block['hash'] = compute_block_hash(block)
        bc.add_block(block)

    print(f"Chain length: {bc.get_chain_length()}")
    print(f"Latest block: {bc.get_latest_block()['index']}")
    print(f"Chain valid: {bc.is_chain_valid()}")


def demo_wallet():
    """Demonstrate Wallet API."""
    print("\n=== Wallet API Demo ===")
    wallet = Wallet()

    # Generate key pairs
    alice = wallet.generate_keys()
    bob = wallet.generate_keys()

    print(f"Alice address: {alice['address']}")
    print(f"Bob address: {bob['address']}")

    # Create transaction
    tx = wallet.create_transaction(
        sender=alice['public_key'],
        recipient=bob['public_key'],
        amount=1.5,
        private_key=alice['private_key']
    )

    # Verify transaction
    valid = wallet.verify_transaction(tx)
    print(f"Transaction valid: {valid}")


def demo_network():
    """Demonstrate P2P Network API."""
    print("\n=== P2P Network API Demo ===")
    network = P2PNetwork()

    peers = network.connect_to_seed_nodes()
    print(f"Connected to {len(peers)} peers")

    # Add custom peer
    network.add_peer("203.0.113.50:8333")
    print(f"Peer count after adding: {network.get_peer_count()}")


def demo_metrics():
    """Demonstrate NetworkAnalyzer API."""
    print("\n=== Metrics API Demo ===")
    bc = Blockchain()
    analyzer = NetworkAnalyzer(bc)

    # Mine a few blocks
    for i in range(1, 6):
        prev = bc.get_latest_block()
        block = {
            "index": i,
            "timestamp": time.time(),
            "data": f"Block {i}",
            "previous_hash": prev.get('hash', compute_block_hash(prev)),
            "transactions": [{"tx": f"tx_{i}"}, {"tx": f"tx_{i+1}"}]
        }
        block['hash'] = compute_block_hash(block)
        bc.add_block(block)
        time.sleep(0.1)

    print(f"Hashrate: {analyzer.calculate_hashrate()} MH/s")
    volume = analyzer.get_transaction_volume()
    print(f"Total TX: {volume['total_transactions']}, TPS: {volume['tps']}")
    analyzer.display_dashboard()


def demo_full_client():
    """Demonstrate the assembled BitcoinCore client."""
    print("\n=== Full Client Demo ===")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "bitcoin_arch", 
        Path(__file__).parent.parent / "Bitcoin-Client-Architecture.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    BitcoinCore = module.BitcoinCore

    client = BitcoinCore()
    client.start()

    # Get status
    status = client.get_status()
    print(f"\nClient status: {status}")


if __name__ == "__main__":
    demo_blockchain()
    demo_wallet()
    demo_network()
    demo_metrics()
    demo_full_client()
    print("\n✅ All demos complete.")
