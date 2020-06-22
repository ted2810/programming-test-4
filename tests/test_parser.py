from unittest import TestCase

from auctionhouse import Auction, Bid, Parser

class ParserTests(TestCase):
  def setUp(self):
    self.parser = Parser()

    self.auction_line_params = ['10', '1', 'SELL', 'toaster_1', '10.00', '20']
    self.bid_line_params = ['12', '8', 'BID', 'toaster_1', '7.50']
    self.heartbeat_line_params = ['16']

  def test_parse(self):
    ...

  def test_is_auction_line(self):
    self.assertIs(
      self.parser.is_auction_line(self.auction_line_params), True
    )
    self.assertIs(
      self.parser.is_auction_line(self.bid_line_params), False
    )
    self.assertIs(
      self.parser.is_auction_line(self.heartbeat_line_params), False
    )

  def test_is_bid_line(self):
    self.assertIs(
      self.parser.is_bid_line(self.auction_line_params), False
    )
    self.assertIs(
      self.parser.is_bid_line(self.bid_line_params), True
    )
    self.assertIs(
      self.parser.is_bid_line(self.heartbeat_line_params), False
    )

  def test_is_heartbeat_line(self):
    self.assertIs(
      self.parser.is_heartbeat_line(self.auction_line_params), False
    )
    self.assertIs(
      self.parser.is_heartbeat_line(self.bid_line_params), False
    )
    self.assertIs(
      self.parser.is_heartbeat_line(self.heartbeat_line_params), True
    )

  def test_get_auction_kwargs(self):
    params = self.auction_line_params

    timestamp = int(params[0])
    user_id = int(params[1])
    item = params[3]
    reserve_price = float(params[4])
    close_time = int(params[5])

    kwargs = self.parser.get_auction_kwargs(params)

    self.assertEqual(kwargs, {
      'timestamp': timestamp,
      'user_id': user_id,
      'item': item,
      'reserve_price': reserve_price,
      'close_time' : close_time
    })

    Auction(**kwargs)

  def test_get_bid_kwargs(self):
    params = self.bid_line_params

    timestamp = int(params[0])
    user_id = int(params[1])
    bid_amount = float(params[4])

    kwargs = self.parser.get_bid_kwargs(params)

    self.assertEqual(kwargs, {
      'timestamp': timestamp,
      'user_id': user_id,
      'bid_amount': bid_amount
    })

    Bid(**kwargs)

  def test_is_valid_bid(self):
    ...
