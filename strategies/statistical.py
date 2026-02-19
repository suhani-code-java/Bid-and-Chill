"""
Statistical Bidding Strategy Module

This module implements a statistical approach to bidding in player auctions.
It uses player statistics and performance metrics to make informed bidding decisions
while managing a total budget across different player roles.

The strategy considers:
- Player base prices
- Performance statistics (batting/bowling averages, economy rates, etc.)
- Star ratings
- Budget allocation per player role
- Current auction dynamics
"""

import random

class StatisticalBiddingStrategy:
    # A default player combination for a team of maximum 11 players.
    DEFAULT_ROSTER_REQUIREMENTS = {
        "batsman": 4,
        "bowler": 4,
        "allrounder": 2,
        "wicketkeeper": 1
    }

    def __init__(self, total_budget):
        """
        Initialize the bidding strategy with a total budget.

        Args:
            total_budget (float): Total capital available (in Cr)
        """
        self.total_budget = total_budget

        # Pull in the default roster requirements.
        roster_requirements = StatisticalBiddingStrategy.DEFAULT_ROSTER_REQUIREMENTS

        # Calculate total number of players needed
        total_players = sum(roster_requirements.values())

        # Budget allocation per position: proportionally allocate the budget.
        self.position_budget = {pos: (total_budget * count / total_players) 
                                  for pos, count in roster_requirements.items()}
        # Start with no spending for any position.
        self.spent_budget = {pos: 0 for pos in roster_requirements}

    def predict_price(self, player):
        """
        Predicts a fair price for a player based on their statistics and performance.

        Args:
            player: Player object with attributes base_price, stats, and role

        Returns:
            float: Predicted fair price for the player

        The model considers:
        - Base price
        - Performance metrics specific to player role
        - Star rating premium/discount
        """
        base = player.base_price
        stars = player.stats.get('stars', 5)  # use a default of 5 if not provided.
        pos = player.role.lower()
        adjustment = 0

        # For batsmen and wicketkeepers: emphasize batting metrics.
        if pos in ['batsman', 'wicketkeeper']:
            bat_avg = player.stats.get('bat_avg', 30)
            strike_rate = player.stats.get('strike_rate', 120)
            # Each 10 runs above a baseline average (30) gives a premium
            # and each 50 points in strike rate above 120 gives additional value.
            adjustment = ((bat_avg - 30) / 10) + ((strike_rate - 120) / 50)
        # For bowlers: emphasize lower bowling average and economy.
        elif pos == 'bowler':
            bowl_avg = player.stats.get('avg', 30)  # lower average is better.
            economy = player.stats.get('economy', 8)
            adjustment = ((30 - bowl_avg) / 10) + ((8 - economy) / 2)
        # For allrounders: combine batting and bowling metrics.
        elif pos == 'allrounder':
            bat_avg = player.stats.get('bat_avg', 25)
            strike_rate = player.stats.get('strike_rate', 120)
            bowl_avg = player.stats.get('bowl_avg', 30)
            economy = player.stats.get('economy', 8)
            batting_adj = ((bat_avg - 25) / 10) + ((strike_rate - 120) / 50)
            bowling_adj = ((30 - bowl_avg) / 10) + ((8 - economy) / 2)
            adjustment = (batting_adj + bowling_adj) / 2

        # Premium based on stars relative to a benchmark rating (5 out of 10).
        star_factor = (stars - 5) * 0.2  # 0.2 Cr premium per star above 5, discount if below.
        predicted = base + adjustment + star_factor
        # Ensure the predicted price is at least the base price.
        return max(predicted, base)

    def allowed_bid(self, player, current_bid):
        """
        Determines the maximum allowed bid for a player based on budget constraints.

        Args:
            player: Player object with role attribute
            current_bid (float): Current auction bid

        Returns:
            float: Maximum allowed bid for the player
        """
        pos = player.role.lower()
        predicted = self.predict_price(player)
        remaining = self.position_budget.get(pos, self.total_budget) - self.spent_budget.get(pos, 0)
        # Use the lower of predicted price and remaining allocated budget.
        allowed = min(predicted, remaining)
        return allowed

    def decide_bid(self, player, current_bid):
        """
        Decides whether and how much to bid for a player.

        Args:
            player: Player object
            current_bid (float): Current auction bid

        Returns:
            float: New bid amount or current bid if holding

        Strategy:
        - Aggressive bidding (0.2 Cr increment) if current bid is below 80% of allowed bid
        - Conservative bidding (0.1 Cr increment) with 30% probability if below allowed bid
        - Hold current bid otherwise
        """
        allowed = self.allowed_bid(player, current_bid)
        if current_bid < 0.8 * allowed:
            new_bid = round(min(current_bid + 0.2, allowed), 2)
        elif current_bid < allowed and random.random() < 0.3:
            new_bid = round(min(current_bid + 0.1, allowed), 2)
        else:
            new_bid = current_bid
        return new_bid

    def update_spent(self, player, winning_bid):
        """
        Updates the spent budget after winning a player bid.

        Args:
            player: Player object with role attribute
            winning_bid (float): Winning bid amount
        """
        pos = player.role.lower()
        if pos in self.spent_budget:
            self.spent_budget[pos] += winning_bid
        else:
            self.spent_budget[pos] = winning_bid

    def evaluate_strategy(self, acquired_players):
        """
        Evaluates the effectiveness of the bidding strategy.

        Args:
            acquired_players (list): List of acquired player objects with winning_bid attributes

        Returns:
            dict: Evaluation metrics including:
                - Total predicted value
                - Total spent budget
                - Position-wise spending
                - Efficiency ratio (value/cost)
        """
        total_predicted_value = 0
        total_spent = 0
        position_spent = {}
        for player in acquired_players:
            predicted = self.predict_price(player)
            total_predicted_value += predicted
            # Expect player to have an attribute 'winning_bid'; fallback to base_price if missing.
            spent = getattr(player, 'winning_bid', player.base_price)
            total_spent += spent
            pos = player.role.lower()
            if pos not in position_spent:
                position_spent[pos] = 0
            position_spent[pos] += spent

        efficiency = total_predicted_value / total_spent if total_spent > 0 else 0.0
        evaluation = {
            "total_predicted_value": total_predicted_value,
            "total_spent": total_spent,
            "position_spent": position_spent,
            "efficiency": efficiency,
        }
        return evaluation
