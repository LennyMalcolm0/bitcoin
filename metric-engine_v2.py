import time
import logging
import json
import os
from abc import ABC, abstractmethod

# --- Sovereign Architecture: Decoupled Components ---

# 1. Advanced Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] Michael Sovereign Analyzer: %(message)s',
    handlers=[
        logging.FileHandler("analyzer_audit.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BlockchainObserver(ABC):
    @abstractmethod
    def on_block_added(self, block):
        pass

class NetworkAnalyzer(BlockchainObserver):
    def __init__(self):
        self.total_transactions = 0
        self.block_times = []
        self.start_monotone = time.monotonic() # High-precision clock, immune to drift
        self.db_path = "network_stats.json"
        self._load_state()

    def _load_state(self):
        """Persistence Layer: Restores state from disk."""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r") as f:
                    data = json.load(f)
                    self.total_transactions = data.get("total_tx", 0)
                    logger.info(f"State restored: {self.total_transactions} txs.")
            except Exception as e:
                logger.error(f"Persistence failure: {e}")

    def _save_state(self):
        """Ensures durability of computed data."""
        try:
            with open(self.db_path, "w") as f:
                json.dump({"total_tx": self.total_transactions}, f)
        except Exception as e:
            logger.error(f"Save failure: {e}")

    def on_block_added(self, block):
        """Observer Hook: Processes new data atomically."""
        tx_count = len(block.get('transactions', []))
        self.total_transactions += tx_count
        self.block_times.append(block.get('timestamp', time.time()))
        
        # Keep window for moving average (last 50 blocks)
        if len(self.block_times) > 50:
            self.block_times.pop(0)
            
        self._save_state()
        logger.info(f"Block {block.get('index')} indexed. Cumulative TXs: {self.total_transactions}")

    def calculate_hashrate(self):
        """Precise Hashrate Estimation (Formula: H = (D * 2^32) / T)"""
        if len(self.block_times) < 2: return 0
        
        duration = self.block_times[-1] - self.block_times[0]
        if duration <= 0: return 0
        
        difficulty = 1 # Simplified for PoC
        hashes = (difficulty * (2**32)) * (len(self.block_times) - 1)
        return round(hashes / duration / 10**6, 2)

    def get_tps(self):
        uptime = time.monotonic() - self.start_monotone
        return round(self.total_transactions / uptime, 4) if uptime > 0 else 0

    def display_report(self):
        print("\n" + "="*40)
        print(f" SOVEREIGN NETWORK DASHBOARD")
        print("-" * 40)
        print(f" Estimated Hashrate : {self.calculate_hashrate()} MH/s")
        print(f" Global TX Volume   : {self.total_transactions}")
        print(f" Real-time TPS      : {self.get_tps()}")
        print("="*40 + "\n")

# --- Sovereign Execution Loop ---

if __name__ == "__main__":
    analyzer = NetworkAnalyzer()
    
    # Simulation of incoming data stream
    try:
        for i in range(1, 6):
            time.sleep(0.5)
            mock_block = {
                "index": i,
                "timestamp": time.time(),
                "transactions": ["tx_" + str(j) for j in range(10)]
            }
            analyzer.on_block_added(mock_block)
            analyzer.display_report()
    except KeyboardInterrupt:
        logger.info("System shutting down gracefully.")
