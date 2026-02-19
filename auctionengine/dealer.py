"""
This module contains the Dealer class which manages the auction process for players.
The Dealer handles player bidding, team assignments, and auction flow control.
"""

import random

class Dealer:
    def __init__(self, players, teams, strategies):
        """
        Initialize the Dealer with players, teams and bidding strategies.

        :param players: List of Player objects representing available players for auction
        :param teams: List of Team objects that will participate in bidding
        :param strategies: Dict mapping team names to their BiddingStrategy objects
        """
        self.players = players
        self.teams = teams
        self.strategies = strategies

    def start_auction(self):
        """
        Start the auction process for all players.
        Players are shuffled randomly to ensure fair auction order.
        """
        # Randomize the order of players for auction
        random.shuffle(self.players)

        # Auction each player one by one
        for player in self.players:
            print(f"\nAuctioning {player.name} ({player.role}) - Base Price: {player.base_price} Cr")
            self.conduct_bidding(player)

    def conduct_bidding(self, player):
        """
        Conduct the bidding process for a single player.
        
        :param player: Player object for whom bidding is being conducted
        """
        current_bid = player.base_price
        highest_bidder = None

        # Continue bidding until no team makes a higher bid
        bidding_active = True
        while bidding_active:
            bidding_active = False
            for team in self.teams:
                # Check if team can participate in bidding
                if team.can_bid(current_bid) and len(team.players) < team.max_players:
                    # Get next bid amount based on team's strategy
                    next_bid = self.strategies[team.name].decide_bid(player, current_bid)
                    # Update highest bid if team can afford it
                    if next_bid > current_bid and team.budget >= next_bid:
                        current_bid = next_bid
                        highest_bidder = team
                        bidding_active = True

        # Finalize the auction for the player
        if highest_bidder:
            player.winning_bid = current_bid  # Set the winning bid amount
            highest_bidder.add_player(player, current_bid)
            print(f"{highest_bidder.name} wins {player.name} for {current_bid} Cr")
        else:
            player.winning_bid = 0.0  # No winning bid
            print(f"No bids placed for {player.name}. Player remains unsold.")