"""
Utility functions for the auction engine.

This module contains utility functions for loading and processing player data.
"""

import pandas as pd
from auctionengine.player import Player

def load_players(filepath, role):
    """
    Load player data from a CSV file and create Player objects.

    Args:
        filepath (str): Path to the CSV file containing player data
        role (str): Player role ('batsman', 'bowler', 'wicketkeeper', 'allrounder')

    Returns:
        list: List of Player objects created from the CSV data
    """
    df = pd.read_csv(filepath).dropna()
    players = []

    for _, row in df.iterrows():
        # Initialize basic stats that are common for all players
        stats_dict = {
            "matches": int(row.get("Matches", 0)),
            "stars": int(row.get("Stars", 0)),
            "age": int(row.get("Age", 0)),
            "span": str(row.get("Span", "")),
        }

        # Add batting stats for batsmen, wicketkeepers, and all-rounders
        if role in ["batsman", "wicketkeeper", "allrounder"]:
            stats_dict.update({
                "runs": int(row.get("Runs", 0)),
                "high_score": str(row.get("High Score", 0)),
                "batting_avg": float(row.get("Average", 0)),
                "strike_rate": float(row.get("Strike Rates", 0)),
                "hundreds": int(row.get("100", 0)),
                "fifties": int(row.get("50", 0)),
                "fours": int(row.get("4s", 0)),
                "sixes": int(row.get("6s", 0)),
                "ducks": int(row.get("Ducks", 0))
            })

        # Add bowling stats for bowlers and all-rounders
        if role in ["bowler", "allrounder"]:
            stats_dict.update({
                "wickets": int(row.get("Wkts", 0)),
                "economy": float(row.get("Economy", 0)),
                "bowling_avg": float(row.get("Avg", 0)),
                "bowling_sr": float(row.get("SR", 0)),
                "four_wickets": int(row.get("4", 0)),
                "five_wickets": int(row.get("5", 0))
            })

        # Add wicketkeeping stats for wicketkeepers
        if role == "wicketkeeper":
            stats_dict.update({
                "catches": int(row.get("Ct", 0)),
                "stumpings": int(row.get("St", 0))
            })

        # Create Player object with all relevant stats and metadata
        player_obj = Player(
            name=row.get("Player"),
            role=role,
            age=int(row.get("Age")),
            nationality=row.get("Nationality"),
            stats=stats_dict,
            base_price=float(row.get("Base Price (Cr)")),
            winning_bid=0.0
        )
        players.append(player_obj)

    return players