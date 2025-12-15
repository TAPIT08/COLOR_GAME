# 🎲 FILIPINO COLOR GAME - QUICK REFERENCE CHEAT SHEET

## 🚀 GETTING STARTED

### Install & Run (3 commands)
```bash
pip install -r requirements.txt    # Install dependencies
streamlit run app.py              # Run web app (RECOMMENDED!)
python main.py                    # Run CLI simulation
```

---

## 🎮 GAME RULES

### Colors
Red | Blue | Yellow | White | Green | Pink

### How to Play
1. Bet on ONE color
2. Roll THREE dice (each shows random color)
3. Count matches → Get payout

### Payouts (for $10 bet)
- **0 matches**: LOSE $10
- **1 match**: WIN $10 (get $20 total)
- **2 matches**: WIN $20 (get $30 total)
- **3 matches**: WIN $30 (get $40 total)

---

## 📊 GAME TYPES

### Fair Game
- All colors: **16.67%** probability
- Standard payouts
- House edge: **~7.87%**

### Tweaked Game
- House color: **20%** probability
- Other colors: **16%** each
- Payouts: **95%** of normal
- House edge: **~11-13%**

**Result**: Players lose **$33.64 more** per 100 games!

---

## 💻 PYTHON CODE EXAMPLES

### 1. Play One Round
```python
from color_game import ColorGame

game = ColorGame(initial_bankroll=1000)
result = game.play_round('Red', bet_amount=10)
print(result)  # Shows: dice, matches, winnings
```

### 2. Run Simulation
```python
from simulation import GameSimulator

simulator = GameSimulator(game)
results = simulator.run_simulation(
    num_simulations=1000,
    rounds_per_game=100,
    bet_amount=10
)
print(f"Mean profit: ${results['net_profit'].mean():.2f}")
```

### 3. Analyze Results
```python
from analysis import GameAnalyzer

analyzer = GameAnalyzer(fair_results, tweaked_results)
stats = analyzer.calculate_summary_statistics()
house_edge = analyzer.calculate_house_edge()
```

### 4. Visualize
```python
from visualization import GameVisualizer

viz = GameVisualizer(fair_results, tweaked_results)
viz.plot_profit_distributions()
viz.plot_house_profit()
```

---

## 🎯 STREAMLIT APP FEATURES

### Sidebar Controls
- 💰 Initial Bankroll: $100-$10,000
- 🔢 Simulations: 100-20,000
- 🎲 Rounds per Game: 10-500
- 💵 Bet Amount: $1-$100
- 🎮 Strategy: Random, Single Color, House Color

### Tweak Parameters
- 🏠 House Color: Select any color
- 📊 House Probability: 16.67%-30%
- 💸 Payout Modifier: 80%-100%

### Analysis Tabs
1. **Profit Distributions** - Histogram, Box, CDF, Density
2. **House Profit** - Distribution & comparison
3. **Win/Loss** - Rates, bankruptcy, rounds played
4. **Cumulative** - Long-term profit trends

### Download Options
- 📥 Fair game CSV
- 📥 Tweaked game CSV
- 📥 Analysis report TXT

---

## 📈 KEY METRICS EXPLAINED

### Player Metrics
- **Mean Profit**: Average $ won/lost per session
- **Win Rate**: % of sessions ending positive
- **Bankruptcy Rate**: % of sessions losing all money

### House Metrics
- **House Profit**: $ earned by casino
- **House Edge**: Profit ÷ Total wagered
- **ROI**: Return on investment %

### Statistical Tests
- **T-Test**: Compare means (parametric)
- **Mann-Whitney U**: Compare distributions (non-parametric)
- **P-Value < 0.05**: Statistically significant difference

---

## 🔬 MATHEMATICAL FORMULAS

### Fair Game Probabilities
```
P(0 matches) = (5/6)³ = 0.5787 = 57.87%
P(1 match)   = 3 × (1/6) × (5/6)² = 0.3472 = 34.72%
P(2 matches) = 3 × (1/6)² × (5/6) = 0.0694 = 6.94%
P(3 matches) = (1/6)³ = 0.0046 = 0.46%
```

### Expected Value (per $1 bet)
```
EV = (0.5787 × -$1) + (0.3472 × $1) + (0.0694 × $2) + (0.0046 × $3)
EV = -$0.0787

House Edge = -EV = 7.87%
```

### House Edge Calculation
```
House Edge = Total House Profit ÷ Total Amount Wagered
```

---

## 🛠️ FILE STRUCTURE

```
COLOR_GAME/
├── app.py              ← Streamlit web app (RUN THIS!)
├── color_game.py       ← Game models (Fair & Tweaked)
├── simulation.py       ← Monte Carlo simulator
├── analysis.py         ← Statistical analysis
├── visualization.py    ← Plotting functions
├── main.py            ← CLI application
├── requirements.txt   ← Dependencies
├── README.md          ← Full documentation
├── DEPLOYMENT.md      ← Deploy to web guide
├── QUICKSTART.py      ← Code examples
├── PROJECT_SUMMARY.md ← Academic overview
└── CHEATSHEET.md      ← This file!
```

---

## 🌐 DEPLOYMENT

### Deploy to Streamlit Cloud (FREE)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Color Game Simulator"
   git push origin main
   ```

2. **Deploy**
   - Go to: https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select repo, set `app.py`
   - Click Deploy!

3. **Your app will be live at:**
   ```
   https://USERNAME-color-game-simulator.streamlit.app
   ```

---

## ⚡ COMMON COMMANDS

### Installation
```bash
pip install numpy pandas matplotlib seaborn scipy tqdm streamlit plotly
```

### Run Applications
```bash
streamlit run app.py              # Web app (port 8501)
streamlit run app.py --server.port 8502  # Different port
python main.py                    # CLI simulation
python QUICKSTART.py              # Examples
```

### Check Versions
```bash
python --version                  # Python version
streamlit --version              # Streamlit version
pip list                         # All packages
```

---

## 🐛 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Import errors | `pip install -r requirements.txt` |
| Port in use | `streamlit run app.py --server.port 8502` |
| Slow simulation | Reduce num_simulations to 1000-5000 |
| Module not found | Check you're in correct directory |
| App won't load | Check requirements.txt & Python 3.8+ |

---

## 📊 TYPICAL RESULTS (10,000 simulations)

### Fair Game
- Mean Loss: **-$78.70**
- Win Rate: **35.2%**
- House Edge: **7.87%**

### Tweaked Game
- Mean Loss: **-$112.34**
- Win Rate: **28.4%**
- House Edge: **11.23%**

### Impact
- Extra Loss: **+$33.64**
- Edge Increase: **+3.36%**
- Win Rate Drop: **-6.8%**

---

## 🎯 BETTING STRATEGIES

### Random
```python
strategy='random'
# Bet on random color each round
```

### Single Color
```python
strategy='single_color'
# Always bet on Red
```

### House Color
```python
strategy='house_color'
# Always bet on the house-favored color
```

---

## 📚 KEY CONCEPTS

### Monte Carlo Simulation
- Run thousands of random trials
- Approximate expected outcomes
- Validate theoretical calculations

### House Edge
- Built-in casino advantage
- Ensures long-term profit
- Works through probability + payouts

### Law of Large Numbers
- More trials → closer to expected value
- Short term: anything can happen
- Long term: math always wins

---

## 🎓 LEARNING OBJECTIVES

✓ Probability distributions  
✓ Expected value calculations  
✓ Monte Carlo methods  
✓ Statistical hypothesis testing  
✓ Data visualization  
✓ Python OOP  
✓ NumPy/Pandas/Matplotlib  
✓ Web app development  

---

## 💡 PRO TIPS

1. **Start Small**: Run 1,000 simulations first to test
2. **Compare Both**: Always run fair AND tweaked together
3. **Use Web App**: Interactive interface is easier than CLI
4. **Export Data**: Download CSV for Excel/further analysis
5. **Adjust Parameters**: Try different house edges to see impact
6. **Read Docs**: Check README.md for complete details

---

## 🔗 RESOURCES

- **Streamlit Docs**: https://docs.streamlit.io
- **NumPy Docs**: https://numpy.org/doc/
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **Matplotlib Docs**: https://matplotlib.org/
- **Monte Carlo**: https://en.wikipedia.org/wiki/Monte_Carlo_method

---

## ⚖️ ACADEMIC USE

✅ **Perfect for:**
- Modeling & Simulation courses
- Statistics projects
- Probability demonstrations
- Data science portfolios
- Monte Carlo tutorials

⚠️ **Remember:**
- Educational purposes only
- Not for actual gambling
- Cite in academic work
- Follow course guidelines

---

## 🎬 QUICK START (3 STEPS)

1. **Install**: `pip install -r requirements.txt`
2. **Run**: `streamlit run app.py`
3. **Simulate**: Click "🚀 Run Simulation" button

**That's it! 🎉**

---

## 📞 HELP

- See **README.md** for full documentation
- See **DEPLOYMENT.md** for hosting guide
- See **QUICKSTART.py** for code examples
- See **PROJECT_SUMMARY.md** for academic context

---

**🎲 Happy Simulating! May the odds be ever in your favor... but they won't be! 📊**

*"The house always wins in the long run" - Mathematics*
