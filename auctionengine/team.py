"""
Team class represents a team in an auction system with a budget and player management capabilities.
"""

class Team:
    def __init__(self, name, budget, max_players):
        """
        Initialize a new team.
        
        Args:
            name (str): Name of the team
            budget (float): Initial budget for player purchases
            max_players (int): Maximum number of players allowed in the team
        """
        self.name = name
        self.budget = budget
        self.max_players = max_players
        self.players = []  # List to store player objects

    def can_bid(self, amount):
        """
        Check if team can afford to bid the specified amount.
        
        Args:
            amount (float): Bid amount to check
            
        Returns:
            bool: True if team has sufficient budget, False otherwise
        """
        return self.budget >= amount

    def add_player(self, player, bid_amount):
        """
        Add a player to the team if budget and squad size constraints are met.
        
        Args:
            player (Player): Player object to add to the team
            bid_amount (float): Amount paid for the player
        """
        if self.can_bid(bid_amount) and len(self.players) < self.max_players:
            self.players.append(player)
            self.budget -= bid_amount  # Deduct bid amount from team budget

    def print_team_summary(self):
        """
        Print a formatted summary of the team including budget and player details.
        """
        print(f"\n--- {self.name} Summary ---")
        print(f"Remaining Budget: {self.budget} Cr")
        print(f"Players in Squad ({len(self.players)}):")
        for p in self.players:
            print(f" • {p.name} ({p.role}) for {p.winning_bid} Cr")
        print("---------------------------\n")
