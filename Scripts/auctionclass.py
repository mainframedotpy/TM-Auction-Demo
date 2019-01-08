class AuctionItem():
    """An Auction Item"""

    def __init__(self, attributes):
        """Pass in detail record from infile on creation
        Input:
        A Sell record as a list
        SELL record format:
        timestamp|user_id|action|item|reserve_price|close_time
        """
        # Create attributes based on input sell record format
        self.starttime = int(attributes[0])
        self.listuser = attributes[1]
        self.name = attributes[3]
        self.reserve = float(attributes[4])
        self.stoptime = int(attributes[5])
        self.open = True
        self.bids = [0]
        self.highbidder = ''
        self.buyprice = 0

    def update_time(self, time):
        """Update item status when a new time is given"""
        # If the time is equal or greater than the stop time
        # and the auction is still open
        if int(time) >= self.stoptime and self.open == True:
            # Close auction and do close processing
            self.open = False
            self.close_auction()

    def new_bid(self, bid):
        """Pass in a bid record and update bids as needed
        Input: 
        A bid record as a list
        BID record format:
        timestamp|user_id|action|item|bid_amount
        """
        # Check if the auction is still open
        if self.open == True:
            # Check if the bid is valid and change highbidder
            if float(bid[4]) > float(max(self.bids)):
                # Check if the bid is greater than the reserve
                # Tells us if someone has won
                if float(bid[4]) > float(self.reserve):
                    self.highbidder = bid[1]
                # Add bid to list of bids 
                self.bids.append(float(bid[4]))
                

    def close_auction(self):
        """Perform processing needed to close the auction and generate
        output data.

        Find buy price, status
        """
        # Check if our item has sold
        # Highbidder is only populated when reserve is met
        if self.highbidder == '':
            self.sold = "UNSOLD"
            self.buyprice = 0
        else: 
            self.sold = "SOLD"
            if float(self.bids[-2]) > float(self.reserve):
                self.buyprice = self.bids[-2]
                # Else the reserve becomes the buy price
            else:
                self.buyprice = self.reserve

        # if there are actual bids other than the dummy init
        # pop the 0 val and set number of bids
        if len(self.bids) > 1: 
            self.bids.pop(0)
            self.nobids = len(self.bids)
        else:
            self.nobids = 0

        print(self.output_record())

    def output_record(self):
        """Build an output record of results
        Return:
        Output Record as a string
        Output format:
        close_time|item|user_id|status|price_paid|total_bid_count|highest_bid|lowest_bid
        """
        # build output record based on parameters
        self.record = (str(self.stoptime) + '|' +
                        str(self.name) + '|' +
                        self.highbidder + '|' +
                        self.sold + '|' +
                        "{:.2f}".format(self.buyprice) + '|' +
                        str(self.nobids) + '|' +
                        "{:.2f}".format(max(self.bids)) + '|' +
                        "{:.2f}".format(min(self.bids))
                        )
        
        return self.record