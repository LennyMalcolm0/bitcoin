import unittest
import time
from metric_engine import NetworkAnalyzer

class MockBlockchain:
    def __init__(self):
        self.chain = []
    def add_block(self, block):
        self.chain.append(block)

class TestNetworkAnalyzer(unittest.TestCase):
    def setUp(self):
        self.blockchain = MockBlockchain()
        self.analyzer = NetworkAnalyzer(self.blockchain)

    def test_initial_hashrate_is_zero(self):
        self.assertEqual(self.analyzer.calculate_hashrate(), 0)

    def test_calculate_hashrate_with_blocks(self):
        # Adding blocks with constant 10s intervals
        for i in range(5):
            self.blockchain.add_block({'timestamp': i * 10, 'transactions': []})
        self.assertGreater(self.analyzer.calculate_hashrate(), 0)

    def test_tps_calculation(self):
        for i in range(10):
            self.blockchain.add_block({
                'timestamp': time.time(),
                'transactions': ['tx'] * 10
            })
        
        stats = self.analyzer.get_transaction_volume()
        self.assertEqual(stats['total_transactions'], 100)
        self.assertGreater(stats['tps'], 0)

if __name__ == '__main__':
    unittest.main()
