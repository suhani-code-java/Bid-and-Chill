Description of the Code
This system implements an auction process for a cricket team selection where different teams bid for available players based on various strategies. Below is a breakdown of the main components and functionality:

1. Dealer Class (auctionengine/dealer.py)
The Dealer class is the core of the auction system. It manages the overall auction flow, including the bidding process, player assignment to teams, and auction completion. Here’s an overview of its components:

_init_(self, players, teams, strategies):

Initializes the dealer with a list of players, teams, and a dictionary of bidding strategies. It sets up everything needed to run the auction.
players: A list of Player objects, representing the available players for auction.
teams: A list of Team objects, representing the teams that will participate in the auction.
strategies: A dictionary where the key is the team name, and the value is the bidding strategy assigned to that team.
start_auction(self):

Starts the auction by randomly shuffling the players and then auctioning each player one by one.
The auction proceeds by calling the conduct_bidding method for each player.
conduct_bidding(self, player):

Conducts the bidding for a specific player.
The bidding is done until no team places a higher bid than the current bid.
Teams are able to place a bid only if they have the funds and available player slots.
The auction ends when the highest bidder is decided for the player.
2. Team Class (auctionengine/team.py)
The Team class handles the team’s budget, players, and maximum player limits. It also has methods to manage bidding participation:

_init_(self, name, budget, max_players):
Initializes a team with a specific name, budget (for bidding), and the maximum number of players that the team can have.
can_bid(self, current_bid):
Checks if the team can participate in the bidding by comparing its budget with the current bid amount.
add_player(self, player, bid):
Adds a player to the team’s roster if the team wins the bid and subtracts the bid amount from the team's budget.
3. Bidding Strategies (strategies/)
Different bidding strategies are implemented in separate files like advanced.py, statistical.py, optimized.py, and others. These strategies define how teams decide the next bid based on a player's stats, the team’s budget, and other factors.

For example:

OptimizedBiddingStrategy: This strategy might be based on maximizing player value within the budget.
StatisticalBiddingStrategy: This could use player statistics (like wickets, runs, etc.) to determine the value of a player and adjust bids accordingly.
Each bidding strategy class needs to implement the decide_bid(player, current_bid) method to calculate the next bid for a player.

4. Player Data (dataset/)
The player data is stored in CSV files categorized by player roles such as batsmen, bowlers, all-rounders, and wicketkeepers. These files contain details about each player, such as:

Player: Player's name
Role: Player's role (e.g., batsman, bowler)
BasePrice: The base price for the player in the auction
Matches: Number of matches played by the player
Wkts: Number of wickets taken by the player (if applicable)
These CSV files are loaded using the load_players() function from auctionengine/utils.py.

5. Main Auction Flow (main.py)
The main.py file is the entry point for running the auction. Here's how it works:

Loading Player Data:

The player data is loaded from CSV files based on player roles (batsmen, bowlers, all-rounders, and wicketkeepers).
The players from all categories are combined into one list for the auction.
Initializing Teams:

Each team is initialized with a specific budget (e.g., 60 Cr) and a maximum number of players allowed (e.g., 15).
The teams are stored in a list for easy access during the auction.
Assigning Bidding Strategies:

Each team is assigned a bidding strategy (e.g., optimized, advanced, statistical). The strategies determine how each team will decide its next bid for players.
Starting the Auction:

The Dealer class is initialized with the players, teams, and bidding strategies.
The auction starts with the dealer.start_auction() method, which proceeds to auction all players.
After the auction, each team's roster and remaining budget are printed out.
6. Example Output
During the auction, the system prints out updates for each player being auctioned. For example:
