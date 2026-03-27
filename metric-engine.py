import time

class NetworkAnalyzer:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.start_time = time.time()

    def calculate_hashrate(self):
        """
        Estimates the network hashrate based on block times.
        Formula: Hashrate = (Difficulty * 2^32) / Time_between_blocks
        """
        if len(self.blockchain.chain) < 2:
            return 0
        
        # Look at the last 5 blocks to get an average
        recent_blocks = self.blockchain.chain[-5:]
        time_elapsed = recent_blocks[-1]['timestamp'] - recent_blocks[0]['timestamp']
        
        if time_elapsed == 0: return 0
        
        # In a real scenario, we'd use actual Difficulty bits
        # Here we use a mock difficulty constant
        mock_difficulty = 1 
        estimated_hashes = (mock_difficulty * (2**32)) * len(recent_blocks)
        hashrate_ps = estimated_hashes / time_elapsed
        
        return round(hashrate_ps / 10**6, 2)  # Return in MH/s

    def get_transaction_volume(self):
        """Returns total transactions and average Transactions Per Second (TPS)."""
        total_tx = sum(len(block.get('transactions', [])) for block in self.blockchain.chain)
        uptime = time.time() - self.start_time
        tps = total_tx / uptime if uptime > 0 else 0
        
        return {
            "total_transactions": total_tx,
            "tps": round(tps, 4)
        }

    def display_dashboard(self):
        stats = self.get_transaction_volume()
        print("\n--- Early Network Statistics ---")
        print(f"Network Hashrate: {self.calculate_hashrate()} MH/s")
        print(f"Total Transactions: {stats['total_transactions']}")
        print(f"Current TPS: {stats['tps']}")
        print("--------------------------------\n")

# --- Integration Example ---

# Assuming 'client.storage' is the Blockchain instance from the previous code
analyzer = NetworkAnalyzer(client.storage)

# Simulate a few 'mining' events
for _ in range(3):
    time.sleep(1) # Simulate time passing
    mock_block = {
        "index": len(client.storage.chain),
        "timestamp": time.time(),
        "transactions": ["tx1", "tx2", "tx3"], # Mock 3 txs per block
        "hash": "..."
    }
    client.storage.add_block(mock_block)
    analyzer.display_dashboard()
