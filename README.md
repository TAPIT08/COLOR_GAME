# Stochastic Game Simulation: Filipino Color Game

A comprehensive Python project exploring **modeling and simulation** of the Filipino "Perya" Color Game using Monte Carlo methods. This project compares a **fair game** with a **tweaked game** that has a house edge to analyze the impact of probabilistic manipulation.

## 📋 Project Overview

This simulation project models a traditional Filipino Color Game and investigates:
- **Probabilistic systems modeling**
- **Monte Carlo simulation** (10,000+ iterations)
- **Exploratory Data Analysis (EDA)**
- **Statistical comparison** of fair vs. tweaked game outcomes
- **House edge quantification**

## 🎲 Game Rules

### Color Game Mechanics
- **Colors**: Red, Blue, Yellow, White, Green, Pink
- **Gameplay**: Players bet on one color, then 3 dice are rolled
- **Payouts**:
  - 0 matches → Lose bet
  - 1 match → 1:1 payout (win equal to bet)
  - 2 matches → 2:1 payout (win 2× bet)
  - 3 matches → 3:1 payout (win 3× bet)

### Game Versions

#### Fair Game
- Each color has equal probability: **1/6 = 16.67%** per die
- Standard payout structure
- Theoretical house edge: ~**7.87%**

#### Tweaked Game (House Edge)
Two modifications create the house advantage:
1. **Weighted Probabilities**: House color (Red) appears **20%** of the time instead of 16.67%
2. **Modified Payouts**: All payouts reduced to **95%** of fair value
   - 1 match: 0.95:1 (instead of 1:1)
   - 2 matches: 1.9:1 (instead of 2:1)
   - 3 matches: 2.85:1 (instead of 3:1)

## 📁 Project Structure

```
COLOR_GAME/
│
├── color_game.py          # Game models (Fair & Tweaked)
├── simulation.py          # Monte Carlo simulation engine
├── analysis.py            # Statistical analysis & EDA
├── visualization.py       # Plotting and charts
├── main.py               # Main application runner
├── requirements.txt      # Python dependencies
├── README.md            # This file
│
└── results/             # Generated output (created on run)
    ├── analysis_report.txt
    ├── profit_distributions.png
    ├── house_profit.png
    ├── win_loss_analysis.png
    ├── bankroll_evolution.png
    ├── fair_game_results.csv
    └── tweaked_game_results.csv
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- `numpy` - Numerical computing and random number generation
- `pandas` - Data manipulation and analysis
- `matplotlib` - Plotting and visualization
- `seaborn` - Statistical data visualization
- `scipy` - Scientific computing and statistical tests
- `tqdm` - Progress bars

## 💻 Usage

### Run Complete Simulation

```powershell
python main.py
```

This will:
1. Create fair and tweaked game models
2. Run 10,000 simulations for each model
3. Perform comprehensive statistical analysis
4. Generate visualizations
5. Save all results to the `results/` folder

### Customize Parameters

Edit [main.py](main.py) to adjust:

```python
INITIAL_BANKROLL = 1000.0      # Starting money
NUM_SIMULATIONS = 10000        # Number of game sessions
ROUNDS_PER_GAME = 100          # Rounds per session
BET_AMOUNT = 10.0              # Bet per round
BETTING_STRATEGY = 'random'    # 'random', 'single_color', 'house_color'

# Tweak parameters
HOUSE_COLOR = 'Red'
HOUSE_COLOR_WEIGHT = 0.20      # Weighted probability
PAYOUT_MODIFIER = 0.95         # Payout reduction factor
```

### Run Streamlit Web App (Recommended!)

For an **interactive web interface** with real-time simulations:

```powershell
streamlit run app.py
```

This launches a web application where you can:
- ⚙️ Adjust simulation parameters with sliders and dropdowns
- 🎲 Run simulations with a button click
- 📊 View interactive visualizations
- 📈 Download results as CSV files
- 🔬 See statistical analysis in real-time

The web app will open automatically in your browser at `http://localhost:8501`

### Use Individual Modules

```python
from color_game import ColorGame, TweakedColorGame
from simulation import GameSimulator

# Create a game
game = ColorGame(initial_bankroll=1000)

# Play a round
result = game.play_round(bet_color='Red', bet_amount=10)
print(result)

# Run simulation
simulator = GameSimulator(game)
results = simulator.run_simulation(
    num_simulations=1000,
    rounds_per_game=100,
    bet_amount=10
)
```

## 🌐 Streamlit Cloud Deployment

### Deploy to Streamlit Community Cloud

1. **Push your code to GitHub**:
   ```powershell
   git init
   git add .
   git commit -m "Filipino Color Game Simulator"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/color-game-simulator.git
   git push -u origin main
   ```

2. **Deploy on Streamlit**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set Main file path: `app.py`
   - Click "Deploy"!

3. **Your app will be live** at: `https://YOUR_USERNAME-color-game-simulator.streamlit.app`

### Configuration for Deployment

The project includes `.streamlit/config.toml` with optimal settings for deployment:
- Custom color theme matching the Color Game aesthetic
- Server configuration for Streamlit Cloud
- Performance optimizations



## 📊 Output & Results

### Generated Files

1. **analysis_report.txt** - Comprehensive statistical report including:
   - Summary statistics (mean, median, std dev)
   - House edge calculations
   - ROI analysis
   - Hypothesis testing results
   - Key findings and conclusions

2. **Visualizations (PNG files)**:
   - `profit_distributions.png` - Histogram, box plot, CDF, and density plots
   - `house_profit.png` - House profit distributions and cumulative totals
   - `win_loss_analysis.png` - Win rates, ROI, and ratio comparisons
   - `bankroll_evolution.png` - Sample game bankroll trajectories

3. **CSV Data Files**:
   - `fair_game_results.csv` - All simulation data for fair game
   - `tweaked_game_results.csv` - All simulation data for tweaked game

### Example Output

```
SIMULATION CONFIGURATION:
  Initial Bankroll:     $1,000.00
  Number of Simulations: 10,000
  Rounds per Game:       100
  Bet Amount:            $10

KEY FINDINGS:
  • The fair game yields an average profit of -$78.70 per session
  • The tweaked game yields an average profit of -$112.34 per session
  • Players lose $33.64 more on average in the tweaked game
  • The house edge increased by 3.364% in the tweaked version
  • Win rate decreased from 35.21% to 28.45%
```

## 🔬 Analysis Features

### Statistical Methods
- **Descriptive Statistics**: Mean, median, standard deviation, min/max
- **Probability Analysis**: Win rates, house edge, ROI
- **Hypothesis Testing**: 
  - Two-sample t-test
  - Mann-Whitney U test (non-parametric)
- **Distribution Analysis**: Skewness, kurtosis, percentiles

### Visualizations
- Profit distribution comparisons
- Cumulative distribution functions (CDF)
- Box plots and density plots
- House profit evolution
- Win/loss rate analysis
- Bankroll trajectory tracking

## 🎯 Learning Objectives

This project demonstrates:
1. **Probabilistic Modeling**: Creating fair and biased random systems
2. **Monte Carlo Methods**: Using repeated random sampling for numerical results
3. **Statistical Analysis**: Comparing distributions and testing hypotheses
4. **Data Visualization**: Communicating results through charts
5. **Python Libraries**: NumPy, Pandas, Matplotlib, SciPy, Seaborn

## 📈 Key Concepts

### House Edge
The house edge is calculated as:
```
House Edge = Total House Profit / Total Amount Wagered
```

For the tweaked game, the house edge is created through:
- **Weighted probabilities** on dice rolls
- **Reduced payouts** compared to fair odds

### Monte Carlo Simulation
By running thousands of simulations, we:
- Approximate the expected value of game outcomes
- Estimate the probability distributions
- Validate theoretical calculations with empirical data
- Quantify variance and risk

## 🛠️ Technical Implementation

### Game Model (`color_game.py`)
- `ColorGame` class: Fair game with equal probabilities
- `TweakedColorGame` class: Inherits from ColorGame, adds weighted dice and modified payouts
- Methods for rolling dice, calculating payouts, tracking history

### Simulation Engine (`simulation.py`)
- `GameSimulator` class: Runs multiple game sessions
- Monte Carlo simulation with configurable parameters
- Progress tracking with tqdm
- Detailed round-level data collection

### Analysis Module (`analysis.py`)
- `GameAnalyzer` class: Statistical computations
- Summary statistics and distributions
- Hypothesis testing
- Comprehensive text report generation

### Visualization Module (`visualization.py`)
- `GameVisualizer` class: Creates publication-quality plots
- Multiple chart types for different insights
- Customizable styling with seaborn
- Automatic saving to files

## 📚 References

- **Monte Carlo Method**: [Wikipedia](https://en.wikipedia.org/wiki/Monte_Carlo_method)
- **House Edge**: [Casino Mathematics](https://en.wikipedia.org/wiki/Casino_game#House_advantage)
- **Filipino Color Game**: Traditional "perya" (fair) gambling game

## 🤝 Contributing

This is an educational project. Feel free to:
- Experiment with different tweak parameters
- Add new betting strategies
- Implement additional game variants
- Enhance visualizations

## 📝 License

This project is created for educational purposes as part of a modeling and simulation course.

## ✨ Author

Created as a demonstration of stochastic modeling and Monte Carlo simulation techniques in Python.

---

**Run the simulation and explore how small changes in probabilities create significant house advantages over thousands of plays!**
