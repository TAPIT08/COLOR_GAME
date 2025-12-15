"""
QUICK START GUIDE
================================================================================

Filipino Color Game Simulator - Get Started in 3 Minutes!

================================================================================
"""

# 1. INSTALL DEPENDENCIES (First Time Only)
# ------------------------------------------
# Open terminal/PowerShell in this directory and run:
#
# pip install -r requirements.txt
#
# This installs: numpy, pandas, matplotlib, seaborn, scipy, tqdm, streamlit


# 2. RUN THE WEB APP (Recommended!)
# ------------------------------------------
# streamlit run app.py
#
# Opens browser automatically at http://localhost:8501
# Use the interactive interface to run simulations


# 3. RUN THE COMMAND-LINE SIMULATION
# ------------------------------------------
# python main.py
#
# Runs 10,000 simulations and saves results to results/ folder
# Takes about 30-60 seconds to complete


# 4. CUSTOMIZE PARAMETERS
# ------------------------------------------
# Edit main.py lines 25-38 to change:
#   - Initial bankroll
#   - Number of simulations  
#   - Bet amounts
#   - House edge tweaks


# 5. USE THE GAME CLASSES DIRECTLY
# ------------------------------------------

from color_game import ColorGame, TweakedColorGame

# Fair game
game = ColorGame(initial_bankroll=1000)
result = game.play_round(bet_color='Red', bet_amount=10)
print(f"Result: {result['net_winnings']}")
print(f"Dice: {result['dice_results']}")

# Tweaked game with house edge
tweaked = TweakedColorGame(
    initial_bankroll=1000,
    house_color='Red',
    house_color_weight=0.20,  # 20% vs fair 16.67%
    payout_modifier=0.95       # 95% of normal payout
)
result = tweaked.play_round(bet_color='Blue', bet_amount=10)


# 6. RUN A CUSTOM SIMULATION
# ------------------------------------------

from simulation import GameSimulator
import pandas as pd

simulator = GameSimulator(game)
results = simulator.run_simulation(
    num_simulations=1000,
    rounds_per_game=100,
    bet_amount=10,
    strategy='random'
)

# Analyze results
print(f"Mean profit: ${results['net_profit'].mean():.2f}")
print(f"Win rate: {(results['net_profit'] > 0).mean():.2%}")
print(f"House profit: ${results['house_profit'].mean():.2f}")


# 7. VISUALIZE RESULTS
# ------------------------------------------

from visualization import GameVisualizer

# Create visualizer
viz = GameVisualizer(fair_results, tweaked_results)

# Generate plots
viz.plot_profit_distributions(save_path='profit_dist.png')
viz.plot_house_profit(save_path='house_profit.png')
viz.plot_cumulative_profit(save_path='cumulative.png')


# 8. STATISTICAL ANALYSIS
# ------------------------------------------

from analysis import GameAnalyzer

analyzer = GameAnalyzer(fair_results, tweaked_results)

# Summary statistics
stats = analyzer.calculate_summary_statistics()
print(stats['fair'])
print(stats['tweaked'])

# House edge
edge = analyzer.calculate_house_edge()
print(f"Fair game edge: {edge['fair']:.4%}")
print(f"Tweaked game edge: {edge['tweaked']:.4%}")

# Hypothesis test
test = analyzer.perform_hypothesis_test()
print(f"P-value: {test['p_value']}")


# 9. EXPORT DATA
# ------------------------------------------

# Save to CSV
results.to_csv('simulation_results.csv', index=False)

# Load back
df = pd.read_csv('simulation_results.csv')


# 10. DEPLOY TO WEB
# ------------------------------------------
# See DEPLOYMENT.md for complete guide
#
# 1. Create GitHub repository
# 2. Push code: git push origin main
# 3. Go to share.streamlit.io
# 4. Click "New app" and select your repo
# 5. Set main file: app.py
# 6. Click Deploy!
#
# Your app will be live at:
# https://YOUR_USERNAME-color-game-simulator.streamlit.app


"""
GAME RULES SUMMARY
================================================================================

COLORS: Red, Blue, Yellow, White, Green, Pink

GAMEPLAY:
1. Player bets on one color
2. Three dice are rolled (each shows a random color)
3. Count how many dice match the player's chosen color

PAYOUTS:
- 0 matches: Lose bet (-$10 if you bet $10)
- 1 match:   Win 1× bet (+$10 if you bet $10)
- 2 matches: Win 2× bet (+$20 if you bet $10)
- 3 matches: Win 3× bet (+$30 if you bet $10)

FAIR GAME:
- All colors equally likely (16.67% each)
- Standard payouts
- Inherent house edge: ~7.87%

TWEAKED GAME:
- House color appears more often (20% instead of 16.67%)
- Payouts reduced to 95% of normal
- Increased house edge: ~11-13%

================================================================================
"""

"""
TROUBLESHOOTING
================================================================================

PROBLEM: ImportError: No module named 'streamlit'
SOLUTION: pip install -r requirements.txt

PROBLEM: Port 8501 already in use
SOLUTION: streamlit run app.py --server.port 8502

PROBLEM: Simulation too slow
SOLUTION: Reduce NUM_SIMULATIONS in main.py (try 1000-5000)

PROBLEM: ModuleNotFoundError: No module named 'color_game'
SOLUTION: Make sure you're in the correct directory with all .py files

PROBLEM: Plots not showing
SOLUTION: Install matplotlib: pip install matplotlib

================================================================================
"""

print("""
================================================================================
  🎲 FILIPINO COLOR GAME SIMULATOR 🎲
================================================================================

Welcome! Choose how to run:

  1. WEB APP (Interactive):    streamlit run app.py
  2. COMMAND LINE:              python main.py
  3. JUPYTER NOTEBOOK:          jupyter notebook
  4. PYTHON SCRIPT:             python your_script.py

For more help, see:
  - README.md - Full documentation
  - DEPLOYMENT.md - Deploy to web guide
  - main.py - Example usage

================================================================================
""")
