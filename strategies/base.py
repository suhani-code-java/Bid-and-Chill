"""
Base bidding strategy implementation for the IPL auction simulator.

This module provides the foundation for creating bidding strategies in the auction.
It includes a basic implementation using a linear regression model to estimate player values
and make bidding decisions.
"""

import random
import numpy as np
from sklearn.linear_model import LinearRegression

class BiddingStrategy:
    """
    Base class for implementing bidding strategies.
    
    This class provides a simple implementation using a linear regression model
    to estimate player values and make bidding decisions. It can be extended
    with more sophisticated ML or RL approaches.
    """

    def __init__(self):
        """
        Initialize the bidding strategy with a simple linear regression model.
        
        The model uses fake coefficients for demonstration purposes.
        In a real implementation, these would be learned from historical data.
        """
        self.model = LinearRegression()
        # Initialize with dummy coefficients for batting average, strike rate, and economy
        self.model.coef_ = np.array([0.1, 0.05, 0.2])  # [bat_avg, strike_rate, economy]
        self.model.intercept_ = 1.0  # Base value for all players

    def estimate_value(self, player):
        """
        Estimate the value of a player based on their statistics.
        
        Args:
            player: Player object containing stats and base price
            
        Returns:
            float: Estimated value of the player in crores
        """
        # Extract key statistics with default values if not available
        bat_avg = player.stats.get('bat_avg', 20)
        strike_rate = player.stats.get('strike_rate', 120)
        economy = player.stats.get('economy', 8)

        # Prepare features for prediction
        X = np.array([[bat_avg, strike_rate, economy]])
        predicted_value = self.model.predict(X)[0]
        
        # Ensure prediction is not below base price
        return max(predicted_value, player.base_price)

    def decide_bid(self, player, current_bid):
        """
        Decide whether to place a bid and how much to bid.
        
        Args:
            player: Player object for whom to make bidding decision
            current_bid: Current highest bid in the auction
            
        Returns:
            float: New bid amount if bidding, otherwise returns current bid
        """
        # Get the estimated value for the player
        estimated_value = self.estimate_value(player)

        # Implement bidding logic
        if current_bid < (0.8 * estimated_value):
            # Aggressive bidding if current bid is significantly below estimated value
            return round(current_bid + 0.2, 2)
        else:
            # Conservative bidding with 30% chance of small increment
            if random.random() < 0.3:
                return round(current_bid + 0.1, 2)
            else:
                return current_bid
            