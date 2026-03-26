import hashlib
import time
import json

class BitcoinComponent:
    """Base class for Bitcoin Core components."""
    def __init__(self, name):
        self.name = name
        print(f"[{self.name}] Initialized.")

class Blockchain(BitcoinComponent):
    def __init__(self):
        super().__init__("Storage & Consensus")
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return {"index": 0, "timestamp": time.time(), "data": "Genesis Block", "hash": "0"}

    def add_block(self, block):
        # In a real client, this involves Proof-of-Work validation
        self.chain.append(block)
        print(f"[{self.name}] New block added to the local ledger.")

class P2PNetwork(BitcoinComponent):
    def __init__(self):
        super().__init__("Networking")
        self.peers = []

    def connect_to_seed_nodes(self):
        # Logic to discover other nodes
        print(f"[{self.name}] Connecting to Bitcoin network peers...")

class Wallet(BitcoinComponent):
    def __init__(self):
        super().__init__("Wallet")
        self.balance = 0.0

    def generate_keys(self):
        print(f"[{self.name}] Generating ECDSA private/public key pair...")

# --- THE ASSEMBLY (Bitcoin Core Client) ---

class BitcoinCore:
    def __init__(self):
        print("--- Starting Bitcoin Core Client ---")
        # Assembling the components
        self.storage = Blockchain()
        self.network = P2PNetwork()
        self.wallet = Wallet()
        
    def start(self):
        print("\n[System] Synchronizing with network...")
        self.network.connect_to_seed_nodes()
        self.wallet.generate_keys()
        
        # Simulate receiving data
        mock_block = {"index": 1, "timestamp": time.time(), "data": "Tx: A->B 0.5 BTC", "hash": "abc123"}
        self.storage.add_block(mock_block)
        
        print("\n[System] Bitcoin Core is running and synchronized.")

if __name__ == "__main__":
    client = BitcoinCore()
    client.start()
