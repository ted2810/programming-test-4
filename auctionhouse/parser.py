from auctionhouse.auction import Auction
from auctionhouse.bid import Bid

class Parser:
  def parse(self, file_path):
    """
    Parses a log file from an auction house and
    returns information about each auction.
    """
    with open(file_path) as input_file:
      # Dictionary that keeps track of all the auctions.
      # An auction can be accessed via the auction item.
      auction_items = {}
      last_heartbeat = None

      for line in input_file:
        line_params = line.split('|')
        current_time = int(line_params[0])

        if self.is_auction_line(line_params):
          # Create auction

          kwargs = self.get_auction_kwargs(line_params)
          auction_item = line_params[3]
          auction = Auction(**kwargs)

          auction_items[auction_item] = auction
        elif self.is_bid_line(line_params):
          # Add bid to auction

          auction_item = line_params[3]
          auction = auction_items[auction_item]

          if auction.is_open:
            kwargs = self.get_bid_kwargs(line_params)
            bid = Bid(**kwargs)

            if self.is_valid_bid(bid, auction):
              auction.bids.append(bid)
        elif self.is_heartbeat_line(line_params):
          # Close inactive auctions

          if last_heartbeat is not None:
            for auction_item in auction_items:
              auction = auction_items[auction_item]

              if auction.is_open:
                bids_since_last_heartbeat = [
                  bid for bid in auction.bids if bid.timestamp > last_heartbeat
                ]

                if not bids_since_last_heartbeat:
                  auction.close()
          last_heartbeat = current_time

        # Close expired auctions
        for auction_item in auction_items:
          auction = auction_items[auction_item]

          if current_time >= auction.close_time and auction.is_open:
            auction.close()

      result = []

      for auction_item in auction_items:
        auction = auction_items[auction_item]

        result.append('|'.join([
          f'{auction.close_time}',
          f'{auction.item}',
          f'{auction.winner_id}',
          f'{auction.status}',
          f'{auction.price_paid:.2f}',
          f'{auction.total_bid_count}',
          f'{auction.highest_bid_amount:.2f}',
          f'{auction.lowest_bid_amount:.2f}'
        ]))

      return result

  def is_auction_line(self, params):
    """
    Accepts the parameters of a line and
    checks if it is an auction line.
    """
    if len(params) > 1 and params[2] == 'SELL':
      return True
    return False

  def is_bid_line(self, params):
    """
    Accepts the parameters of a line and
    checks if it is a bid line.
    """
    if len(params) > 1 and params[2] == 'BID':
      return True    
    return False
  
  def is_heartbeat_line(self, params):
    """
    Accepts the parameters of a line and
    checks if it is a heartbeat line.
    """
    if len(params) == 1:
      return True
    return False

  def get_auction_kwargs(self, params):
    """
    Accepts the parameters of an auction line
    and returns the arguments for a new Auction() object.
    """
    timestamp = int(params[0])
    user_id = int(params[1])
    item = params[3]
    reserve_price = float(params[4])
    close_time = int(params[5])

    return {
      'timestamp': timestamp,
      'user_id': user_id,
      'item': item,
      'reserve_price': reserve_price,
      'close_time' : close_time
    }

  def get_bid_kwargs(self, params):
    """
    Accepts the parameters of a bid line
    and returns the arguments for a new Bid() object.
    """
    timestamp = int(params[0])
    user_id = int(params[1])
    bid_amount = float(params[4])

    return {
      'timestamp': timestamp,
      'user_id': user_id,
      'bid_amount': bid_amount
    }

  def is_valid_bid(self, bid, auction):
    """
    Validates a bid against an auction.

    A bid is valid if:
    - it arrives after the auction's start time
    - before or on the auction's closing time
    - is larger than any previous valid bids by the same user
    """
    if auction.timestamp < bid.timestamp <= auction.close_time:
      if not auction.bids:
        return True

      user_bids = [
        auction_bid for auction_bid in auction.bids
          if auction_bid.user_id == bid.user_id
      ]

      if not user_bids:
        return True

      sorted_user_bids = sorted(user_bids, key=lambda bid: bid.bid_amount)
      highest_user_bid = sorted_user_bids[-1]

      if highest_user_bid.bid_amount < bid.bid_amount:
        return True      

    return False
