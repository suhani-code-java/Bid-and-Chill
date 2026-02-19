import random
import pandas as pd

# Player class to store player information
class Player:
    def __init__(self, name, role, nationality, base_price, stats):
        # Ensure role matches the team structure (lowercase)
        role_map = {
            'batsmen': 'batsman',
            'bowlers': 'bowler',
            'allrounders': 'allrounder',
            'wicketkeepers': 'wicketkeeper'
        }
        self.name = name
        self.role = role_map.get(role, role)  # Map to correct role
        self.nationality = nationality
        self.base_price = base_price
        self.stats = stats  # Includes stars, nationality, etc.

# Optimized Bidding Strategy Class
class OptimizedBiddingStrategy2:
    ROLE_REQUIREMENTS = {"batsman": 4, "bowler": 4, "allrounder": 4, "wicketkeeper": 2}
    MAX_FOREIGN_PLAYERS = 4  # Maximum number of foreign players in the team

    def __init__(self, total_budget):
        self.total_budget = total_budget
        self.remaining_budget = total_budget
        self.team = {"batsman": 0, "bowler": 0, "allrounder": 0, "wicketkeeper": 0, "foreign_players": 0}
        self.players_acquired = []
        self.players_data = self.load_players_data()

    def load_players_data(self):
        """
        Loads player data from the CSV files and returns a list of Player objects.
        """
        players_data = []
        for role in ['batsmen', 'bowlers', 'allrounders', 'wicketkeepers']:
            df = pd.read_csv(f"dataset/{role}.csv")  # Assuming files in the dataset folder

            df.columns = df.columns.str.strip()  # Strip spaces from column names
            
            for _, row in df.iterrows():
                player = Player(
                    name=row['Player'],  # Column name in your dataset
                    role=role,  # Role inferred from file name (batsmen, bowlers, etc.)
                    nationality=row['Nationality'],
                    base_price=row['Base Price (Cr)'],  # Correct column name for base price
                    stats={"stars": row['Stars']}  # Assuming Stars column exists
                )
                players_data.append(player)
        
        return players_data

    def is_valid_bid(self, player, current_bid):
        if current_bid > self.remaining_budget:
            return False
        if player.nationality != "I" and self.team["foreign_players"] >= self.MAX_FOREIGN_PLAYERS:
            return False
        return True

    def estimate_value(self, player):
        base = player.base_price
        stars = player.stats.get("stars", 5)
        
        star_factor = (stars - 5) * 0.4
        estimated_value = base + star_factor

        if stars >= 8:
            estimated_value *= 1.2

        # Apply synergy factor
        synergy_factor = self.calculate_synergy(player)
        estimated_value *= synergy_factor

        return max(estimated_value, base)

    def calculate_synergy(self, player):
        synergy_score = 1.0
        # Ensure the role is in lowercase to match the team dictionary keys
        if self.team[player.role] < self.ROLE_REQUIREMENTS.get(player.role, 0):
            synergy_score += 0.2
        if player.nationality == "I" and self.team["foreign_players"] > 3:
            synergy_score += 0.1
        return synergy_score

    def decide_bid(self, player, current_bid):
        if not self.is_valid_bid(player, current_bid):
            return current_bid

        estimated_value = self.estimate_value(player)
        budget_factor = self.remaining_budget / self.total_budget
        
        role_needed = self.team[player.role] < self.ROLE_REQUIREMENTS.get(player.role, 0)

        if role_needed and current_bid < 0.95 * estimated_value:
            return round(min(current_bid + 0.6, estimated_value * budget_factor), 2)

        if player.stats.get("stars", 5) >= 8 and current_bid < estimated_value:
            return round(min(current_bid + 0.4, estimated_value * budget_factor), 2)

        if current_bid < estimated_value and random.random() < 0.4 * budget_factor:
            return round(min(current_bid + 0.2, estimated_value * budget_factor), 2)

        # Ensure next bid >= current bid if remaining budget is low
        if self.remaining_budget < self.total_budget * 0.1:
            return max(current_bid, round(current_bid + 0.1, 2))

        return current_bid

    def update_team(self, player, winning_bid):
        self.players_acquired.append(player)
        self.remaining_budget -= winning_bid
        self.team[player.role] += 1
        if player.nationality != "I":
            self.team["foreign_players"] += 1

    def get_player_by_name(self, player_name):
        """
        Retrieves player details by name from the loaded players data.
        """
        for player in self.players_data:
            if player.name == player_name:
                return player
        return None

def get_next_bid_value(player_name,  current_bid,purse_left):
    """
    Determines the next bid value for a given player based on the strategy.

    Parameters:
    - player_name (str): Name of the player being bid on.
    - purse_left (float): The remaining budget for bidding.
    - current_bid (float): The current highest bid for the player.

    Returns:
    - float: The next bid value or the current bid if no further bid is advisable.
    """
    strategy = OptimizedBiddingStrategy2(total_budget=60)  # Adjust total budget to 60 Cr as per constraint

    # Get player object from strategy's dataset
    player = strategy.get_player_by_name(player_name) 

    if not player:
        print(f"Player {player_name} not found.")
        return current_bid

    # Temporarily adjust the strategy's remaining budget
    strategy.remaining_budget = purse_left
    ans = strategy.decide_bid(player, current_bid)
    if ans > current_bid:
        return ans
    else :
        return 0


