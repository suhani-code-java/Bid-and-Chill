"""
Player class represents a cricket player in the auction system.
"""

class Player:
    def __init__(self, name, role, age, nationality, stats, base_price, winning_bid):
        """
        Initialize a new Player instance.

        Args:
            name (str): Full name of the player
            role (str): Player's role (e.g., batsman, bowler, all-rounder)
            age (int): Player's age
            nationality (str): Player's country of origin
            stats (dict): Dictionary containing player's performance statistics
            base_price (float): Starting bid price for the player
        """
        self.name = name
        self.role = role
        self.age = age
        self.nationality = nationality
        self.stats = stats
        self.base_price = base_price
        self.winning_bid = 0.0

    def __str__(self):
        """
        Returns a string representation of the Player.

        Returns:
            str: Player's name and role in format 'name - role'
        """
        return f"{self.name} - {self.role}"
        