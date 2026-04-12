import time

class NetworkAnalyzer:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        # Using monotone clock for precision performance measuring
        self.start_time_mono = time.monotonic()
        # Cache for cumulative counts to avoid re-summing entire chain (O(1) instead of O(n))
        self._cached_tx_count = 0
        self._last_processed_index = -1
        self._last_processed_hash = None
        # Sliding window for hashrate
        self._window_size = 5

    def _sync_cache(self):
        """O(k) where k is new blocks since last check, instead of O(n)"""
        current_chain = self.blockchain.chain
        
        # Handle blockchain reorganizations safely by checking the last processed block hash
        is_reorg = len(current_chain) <= self._last_processed_index
        if not is_reorg and self._last_processed_index >= 0:
            if current_chain[self._last_processed_index].get('hash') != self._last_processed_hash:
                is_reorg = True

        if is_reorg:
            self._cached_tx_count = 0
            self._last_processed_index = -1
            self._last_processed_hash = None

        for i in range(self._last_processed_index + 1, len(current_chain)):
            self._cached_tx_count += len(current_chain[i].get('transactions', []))
            self._last_processed_index = i
            self._last_processed_hash = current_chain[i].get('hash')

    def calculate_hashrate(self):
        """Optimized hashrate calculation with reorg safety."""
        chain_len = len(self.blockchain.chain)
        if chain_len < 2:
            return 0
        
        start_idx = max(0, chain_len - self._window_size)
        recent_blocks = self.blockchain.chain
        
        time_elapsed = recent_blocks[chain_len-1]['timestamp'] - recent_blocks[start_idx]['timestamp']
        if time_elapsed <= 0: 
            return 0
        
        # Fix: The time elapsed covers (N-1) block intervals.
        # N = chain_len - start_idx. Intervals = N - 1.
        intervals = (chain_len - 1) - start_idx
        if intervals <= 0:
            return 0

        # Constant folded bit shift (2^32 hashes per block)
        estimated_hashes = (1 << 32) * intervals
        hashrate_ps = estimated_hashes / time_elapsed
        
        return round(hashrate_ps / 1_000_000, 2)

    def get_transaction_volume(self):
        """O(1) retrieval after sync."""
        self._sync_cache()
        uptime = time.monotonic() - self.start_time_mono
        tps = self._cached_tx_count / uptime if uptime > 0 else 0
        
        return {
            "total_transactions": self._cached_tx_count,
            "tps": round(tps, 4)
        }

    def display_dashboard(self):
        stats = self.get_transaction_volume()
        print(f"\n--- Optimized Network Statistics ---\n"
              f"Network Hashrate: {self.calculate_hashrate()} MH/s\n"
              f"Total Transactions: {stats['total_transactions']}\n"
              f"Current TPS: {stats['tps']}\n"
              f"------------------------------------\n")

if __name__ == "__main__":
    print("Sovereign Engine Optimized Node ready.")
