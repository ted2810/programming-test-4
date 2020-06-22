class Auction:
  def __init__(
    self,
    timestamp,
    user_id,
    item,
    reserve_price,
    close_time
  ):
    self.timestamp = timestamp
    self.user_id = user_id
    self.item = item
    self.reserve_price = reserve_price
    self.close_time = close_time

    self.bids = []
    self.is_open = timestamp < close_time

  @property
  def status(self):
    """
    The status of an auction ('SOLD' or 'UNSOLD').
    """
    if (not self.is_open
        and self.bids
        and self.highest_bid.bid_amount >= self.reserve_price):
      return 'SOLD'
    return 'UNSOLD'

  @property
  def price_paid(self):
    """
    The paid price.

    The amount is:
    - The 2nd highest bid price if there have been 2+ bids >= the reserve price.
    - The reserve price if there has been only 1 bid >= reserve price.
    - 0.00 otherwise
    """
    if self.status == 'SOLD':
      if len(self.bids) == 1:
        return self.reserve_price
      elif len(self.bids) > 1:
        highest_bid_index = self.bids.index(self.highest_bid)
        return self.bids[highest_bid_index - 1].bid_amount
    return 0.00

  @property
  def total_bid_count(self):
    """
    The total bid count.
    """
    return len(self.bids)

  @property
  def winner_id(self):
    """
    The winner ID or None if there hasn't been a winner.
    """
    return self.highest_bid.user_id if self.status == 'SOLD' else ''

  @property
  def highest_bid(self):
    """
    The highest bid.

    If there have been 2+ bids with the same amount,
    the earliest bid is the highest bid.
    """
    if self.bids:
      bids = sorted(self.bids, key=lambda bid: bid.bid_amount)
      last_bid = bids[-1]
      highest_bids = [
        bid for bid in bids if bid.bid_amount == last_bid.bid_amount
      ]

      return sorted(highest_bids, key=lambda bid: bid.timestamp)[0]

  @property
  def lowest_bid(self):
    """
    The lowest bid.

    If there have been 2+ bids with the same amount,
    the earliest bid is the lowest bid.
    """
    if self.bids:
      bids = sorted(self.bids, key=lambda bid: bid.bid_amount)
      first_bid = bids[0]
      lowest_bids = [
        bid for bid in bids if bid.bid_amount == first_bid.bid_amount
      ]

      return sorted(lowest_bids, key=lambda bid: bid.timestamp)[0]

  @property
  def highest_bid_amount(self):
    """
    The highest bid amount of 0.00 if there haven't been any bids.
    """
    return self.highest_bid.bid_amount if self.highest_bid else 0.00

  @property
  def lowest_bid_amount(self):
    """
    The lowest bid amount or 0.00 if there haven't been any bids.
    """
    return self.lowest_bid.bid_amount if self.lowest_bid else 0.00

  def close(self):
    """
    Closes the auction.
    """
    self.is_open = False
