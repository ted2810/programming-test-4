from unittest import TestCase

from auctionhouse import Auction, Bid

class AuctionTests(TestCase):
  def setUp(self):
    self.auction = Auction(1, 1, 'toaster_1', 10.00, 12)

  def test_auction_instance(self):
    self.assertEqual(self.auction.timestamp, 1)
    self.assertEqual(self.auction.user_id, 1)
    self.assertEqual(self.auction.item, 'toaster_1')
    self.assertEqual(self.auction.reserve_price, 10.00)
    self.assertEqual(self.auction.close_time, 12)

    self.assertEqual(self.auction.bids, [])
    self.assertIs(self.auction.is_open, True)

  def test_status_with_an_open_auction(self):
    self.assertEqual(self.auction.status, 'UNSOLD')

  def test_status_with_no_bids(self):
    self.auction.close()
    self.assertEqual(self.auction.status, 'UNSOLD')

  def test_status_with_an_insufficient_highest_bid(self):
    bid = Bid(2, 2, 7.50)

    self.auction.bids.append(bid)
    self.auction.close()

    self.assertLessEqual(bid.bid_amount, self.auction.reserve_price)
    self.assertEqual(self.auction.status, 'UNSOLD')

  def test_status_with_a_sufficient_highest_bid(self):
    bid = Bid(2, 2, 15.00)

    self.auction.bids.append(bid)
    self.auction.close()

    self.assertLessEqual(self.auction.reserve_price, bid.bid_amount)
    self.assertEqual(self.auction.status, 'SOLD')


  def test_price_paid_with_no_bids(self):
    ...

  def test_price_paid_with_insufficient_bid(self):
    ...

  def test_price_paid_with_sufficient_bid(self):
    ...

  def test_total_bid_count(self):
    ...

  def test_winner_id(self):
    ...

  def test_highest_bid_with_no_bids(self):
    self.assertIs(self.auction.highest_bid, None)

  def test_highest_bid_with_one_bid(self):
    bid = Bid(2, 2, 7.50)
    self.auction.bids.append(bid)
    self.assertIs(self.auction.highest_bid, bid)

  def test_highest_bid_with_ordered_bids(self):
    low_bid = Bid(2, 2, 7.50)
    high_bid = Bid(3, 3, 9.00)

    self.auction.bids.append(low_bid)
    self.auction.bids.append(high_bid)

    self.assertIs(self.auction.highest_bid, high_bid)

  def test_highest_bid_with_unordered_bids(self):
    high_bid = Bid(2, 2, 9.00)
    low_bid = Bid(3, 3, 7.50)

    self.auction.bids.append(high_bid)
    self.auction.bids.append(low_bid)

    self.assertIs(self.auction.highest_bid, high_bid)

  def test_lowest_bid(self):
    ...

  def test_highest_bid_amount(self):
    ...

  def test_lowest_bid_amount(self):
    ...

  def test_close(self):
    self.auction.close()
    self.assertIs(self.auction.is_open, False)
