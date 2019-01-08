# Import useful modules
import sys
from auctionclass import AuctionItem

# Get infile from run command
infile = sys.argv[1]

def get_timeline(infile):
    """Read bid/sell details from infile
    Return as a list of lists
    Input split on '|'
    """
    with open(infile, 'r') as file:
        read_out = []
        # Read each line into an array, remove trailing new lines
        # split each line on the pipe delimiter
        for line in file:
            read_out.append(line.rstrip("\n").split('|'))
    return read_out


# Your program starts here
def main():
    listactions = get_timeline(infile)
    open_auction, closed_auction = [], []

    # Loop through all input records
    for record in listactions:
        # Use a try/except/finally, hearbeat records might hit an index error
        # We want to update time no matter what record we get
        try:
            # Deal will sell records first since there might not be any open items
            if record[2] == "SELL":
                # Init new auction item in list from input record 
                open_auction.append(AuctionItem(record[:]))
            # Loop though all items and perform bids and heartbeats
            for item in open_auction:
                # if item name matches bid name, input a new bid
                if record[2] == "BID" and item.name == record[3]:
                    item.new_bid(record)

        # Will hit an index error on heartbeat messages
        except IndexError:
            # This was doing a bit more before but is just a pass now
            pass

        finally:
            # Update time for any open auctions
            for item in open_auction:
                item.update_time(record[0])
                # If the item is closed, add to closed items list
                if not item.open == True:
                    closed_auction.append(item)
            # Renew open auctions to be a list of only open auctions (open = True)
            # list comp might get memory intense on a large set of auctions
            open_auction = [x for x in open_auction if x.open == True]


if __name__ == "__main__":
    main()