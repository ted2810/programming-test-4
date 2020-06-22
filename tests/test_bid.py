from unittest import TestCase

from auctionhouse import Bid

class BidTests(TestCase):
  def test_bid_instance(self):
    timestamp = 1
    user_id = 1
    bid_amount = 10.00

    bid = Bid(timestamp, user_id, bid_amount)
    
    self.assertEqual(bid.timestamp, timestamp)
    self.assertEqual(bid.user_id, user_id)
    self.assertEqual(bid.bid_amount, bid_amount)
