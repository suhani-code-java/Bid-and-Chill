![Banner](images/dream-team-challenge.png)

Welcome to Dream Team Challenge. 

This repository contains code and data to simulate an auction-based transfer market. In the auction, multiple teams bid on players using different bidding strategies. This README provides a complete overview of the data, example bidding strategies, repository layout, and instructions for running the code.

## 1. Dataset Description
The project uses four datasets representing various player types: **batsmen**, **bowlers**, **wicketkeepers**, and **allrounders**. Each CSV file contains detailed statistics about players, which are used to drive the auction simulation.

### Data Sources
- **batsmen.csv**: Contains batting-centric statistics for cricketers recognized as batsmen.
- **bowlers.csv**: Contains bowling-specific metrics for cricketers recognized as bowlers.
- **wicketkeepers.csv**: Contains both batting and wicketkeeping data.
- **allrounders.csv**: Contains all-rounder statistics, including both batting and bowling metrics.

Data is sourced from reputable cricket statistics providers and has been preprocessed (cleaned, type-converted, missing values addressed) before being loaded during the simulation.

### Column Definitions Table
Below is a sample table explaining key columns from the datasets. (Similar tables exist for bowlers, wicketkeepers, and allrounders.)

| Column Name      | Data Type | Units/Format   | Significance                                          |
|------------------|-----------|----------------|-------------------------------------------------------|
| Player           | String    | —              | Full name of the player.                              |
| Stars            | Integer   | —              | Calculated Rating of the player (subjective performance indicator). |
| Nationality      | String    | —              | Country code (e.g., I for India, F for Foreign).      |
| Age              | Integer   | years          | Current age of the player.                            |
| Span             | String    | YYYY-YYYY      | Playing period.                                       |
| Matches          | Integer   | —              | Number of matches played.                             |
| Not - Out        | Integer   | —              | Number of times remained not out.                     |
| Runs             | Integer   | runs           | Total runs scored by the player.                      |
| High Score       | String    | runs or runs*   | Highest score in an innings (an asterisk indicates unbeaten innings). |
| Average          | Float     | runs           | Batting average calculated as total runs divided by dismissals. |
| Ball Faced       | Integer   | balls          | Total number of balls faced.                          |
| Strike Rates     | Float     | runs/100 balls | Efficiency rate in scoring runs.                      |
| 100 / 50         | Integer   | —              | Number of centuries and half-centuries respectively.  |
| Ducks            | Integer   | —              | Number of innings with zero runs.                     |
| 4s and 6s        | Integer   | count          | Number of boundaries scored.                          |
| Base Price (Cr)  | Float     | Crore          | Starting bid price in crores.                         |

Similar definitions and units apply to bowling metrics (e.g., Wickets, Economy, Overs) and additional fields for wicketkeeping (e.g., Dismissed, Ct, St) as well as allrounder specific metrics.

## 2. Bidding Strategies
The project demoes multiple bidding strategies for teams to decide how much to bid for a player. Each strategy can be thought of as an algorithm that may/may not take player characteristics (e.g., base price, performance statistics) and team constraints (e.g., remaining budget, squad size) into account.

### Example Bidding Strategies
1. **Base Strategy**  
    - **Working:** This strategy uses a simple linear regression model to estimate a player's value from key performance metrics (batting average, strike rate, and economy). It then compares the current bid with the estimated value: if the current bid is less than 80% of the estimated value, it increases the bid by 0.2 Cr; otherwise, it may increment by 0.1 Cr with a 30% probability.  
    - **Strengths:** Leverages performance data for dynamic bid adjustments.  
    - **Weaknesses:** The simplified regression model goes all in with the budgets for a player and also may not capture all nuances of a player's performance.  
    - **Location:** See file `strategies/base.py`

2. **Statistical Strategy**  
    - **Working:** This strategy leverages a heuristic statistical model tailored by player role. For batsmen and wicketkeepers, it emphasizes batting metrics; for bowlers and allrounders, it combines bowling and batting performance. It also manages bid increments based on a position-specific remaining budget. Namely, if the current bid is less than 80% of the allowed bid (determined by the statistical model and allocated budget), it increases by 0.2 Cr; otherwise, it may add 0.1 Cr with a 30% chance.
    - **Strengths:** Combines statistical price prediction with budget management tailored to specific player roles.  
    - **Weaknesses:** Can be overly conservative if the allocated budget for a position is nearly exhausted.  
    - **Location:** See file `strategies/statistical.py`

Each team in the auction simulation is assigned a bidding strategy which helps determine its next bid for a player. The Dealer (auction manager) uses these strategies by calling a method (e.g., `decide_bid()`) on the bidding strategy object corresponding to a team.

## 3. Repository File Structure
Below is an overview of the repository structure and a brief explanation of key files and directories:

```
├── auctionengine/  
│   ├── dealer.py         -> Manages overall auction process, shuffling players and conducting bidding rounds.  
│   ├── team.py           -> Defines the Team class; stores team details such as budget, player list etc.  
│   ├── player.py         -> Defines the Player class which encapsulates player attributes and string representations.  
│   └── utils.py          -> Contains helper functions to load and preprocess player data from CSV files.  
├── dataset/  
│   ├── batsmen.csv       -> Batting-centric performance metrics for batsmen.  
│   ├── bowlers.csv       -> Bowling metrics for bowlers.  
│   ├── wicketkeepers.csv -> Combined batting and wicketkeeping data for wicketkeepers.  
│   └── allrounders.csv   -> Dual-role performance metrics for allrounders.  
├── strategies/  
│   ├── base.py           -> Implementation of a simple linear regression strategy.  
│   ├── statistical.py    -> Implementation of heuristic stats based strategy.   
└── requirements.txt      -> Lists the Python package dependencies.
```

## 4. Dependencies
The project is built using Python 3.8+ and depends on the following packages:
- Python 3.12
- Pandas  
- Numpy
- Scikit-learn

To install the dependencies, run:
```bash
pip install -r requirements.txt
```
## 5. Running the Simulation
After installing the dependencies, to run the simulated auction, execute the following command:
```bash
python auction.py
```
This command will initialize the Dealer, load player data from the CSV files in the `dataset` folder via `utils.py`, assign teams and strategies, and commence the auction process.
