import unittest
import time
from metric_engine import NetworkAnalyzer

class MockBlockchain:
    def __init__(self):
        self.chain = []
    
    def add_block(self, block):
        # Automatically add hash if missing for testing reorg logic
        if 'hash' not in block:
            block['hash'] = f"hash_{len(self.chain)}"
        self.chain.append(block)

class TestNetworkAnalyzer(unittest.TestCase):
    def setUp(self):
        self.blockchain = MockBlockchain()
        self.analyzer = NetworkAnalyzer(self.blockchain)

    def test_initial_hashrate_is_zero(self):
        self.assertEqual(self.analyzer.calculate_hashrate(), 0)

    def test_calculate_hashrate_valid_chain(self):
        # Add 5 blocks, 10 seconds apart
        # Monotonic time used for internal consistency
        start_ts = time.monotonic()
        for i in range(5):
            self.blockchain.add_block({
                'timestamp': start_ts + (i * 10),
                'transactions': ['tx'] * 10
            })
        
        hashrate = self.analyzer.calculate_hashrate()
        self.assertGreater(hashrate, 0)
        # 4 intervals * (1<<32) / 40 seconds = 429496729.6 H/s ~= 429.5 MH/s
        self.assertAlmostEqual(hashrate, 429.5, places=1)

    def test_transaction_volume_caching(self):
        start_ts = time.monotonic()
        for i in range(3):
            self.blockchain.add_block({
                'timestamp': start_ts + (i * 10),
                'transactions': ['tx'] * 5
            })
        
        stats = self.analyzer.get_transaction_volume()
        self.assertEqual(stats['total_transactions'], 15)
        
        # Add more blocks
        for i in range(2):
            self.blockchain.add_block({
                'timestamp': start_ts + (30 + i * 10),
                'transactions': ['tx'] * 5
            })
            
        stats = self.analyzer.get_transaction_volume()
        self.assertEqual(stats['total_transactions'], 25)

    def test_reorg_detection(self):
        start_ts = time.monotonic()
        for i in range(5):
            self.blockchain.add_block({
                'timestamp': start_ts + (i * 10),
                'transactions': ['tx'] * 10
            })
            
        # Initial sync
        self.analyzer.get_transaction_volume()
        self.assertEqual(self.analyzer._cached_tx_count, 50)
        
        # Simulate reorg: same length, different hash at tip
        self.blockchain.chain[4] = {
            'timestamp': start_ts + 40,
            'transactions': ['tx'] * 5,
            'hash': 'NEW_HASH'
        }
        
        self.analyzer.get_transaction_volume()
        # Cache should reset and re-sum: 10+10+10+10+5 = 45
        self.assertEqual(self.analyzer._cached_tx_count, 45)

if __name__ == "__main__":
    unittest.main()
