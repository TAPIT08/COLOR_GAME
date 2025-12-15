# 🚀 Streamlit Deployment Guide

## Quick Start (Local)

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Run the App
```powershell
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 🌐 Deploy to Streamlit Community Cloud (FREE!)

### Prerequisites
- GitHub account
- Streamlit Community Cloud account ([share.streamlit.io](https://share.streamlit.io))

### Step-by-Step Deployment

#### Step 1: Prepare Your Repository

1. **Create a GitHub repository**:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: Filipino Color Game Simulator"
   ```

2. **Push to GitHub**:
   ```powershell
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/color-game-simulator.git
   git branch -M main
   git push -u origin main
   ```

#### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign in with GitHub"**
3. Click **"New app"**
4. Fill in the deployment form:
   - **Repository**: Select your `color-game-simulator` repo
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**

#### Step 3: Wait for Deployment

- First deployment takes 2-5 minutes
- Subsequent updates are automatic when you push to GitHub
- Your app will be live at: `https://YOUR_USERNAME-color-game-simulator.streamlit.app`

---

## 📁 Required Files for Deployment

Ensure these files are in your repository:

✅ `app.py` - Main Streamlit application  
✅ `requirements.txt` - Python dependencies  
✅ `color_game.py` - Game model classes  
✅ `simulation.py` - Monte Carlo simulator  
✅ `analysis.py` - Statistical analysis  
✅ `visualization.py` - Plotting functions  
✅ `.streamlit/config.toml` - Streamlit configuration  
✅ `.gitignore` - Git ignore patterns  
✅ `README.md` - Documentation  

---

## ⚙️ Configuration

The `.streamlit/config.toml` file contains:

```toml
[theme]
primaryColor="#FF6B6B"        # Main accent color
backgroundColor="#FFFFFF"      # Background color
secondaryBackgroundColor="#F0F2F6"  # Sidebar background
textColor="#262730"           # Text color
font="sans serif"             # Font family

[server]
headless = true               # Required for deployment
port = 8501                   # Local port
enableXsrfProtection = true   # Security

[browser]
gatherUsageStats = false      # Privacy
```

---

## 🔧 Troubleshooting

### Import Errors
- **Issue**: `ModuleNotFoundError: No module named 'streamlit'`
- **Solution**: Install requirements: `pip install -r requirements.txt`

### Port Already in Use
- **Issue**: `OSError: [Errno 98] Address already in use`
- **Solution**: 
  ```powershell
  streamlit run app.py --server.port 8502
  ```

### App Won't Load
- **Issue**: Streamlit Cloud shows "Application error"
- **Solutions**:
  1. Check that `requirements.txt` includes all dependencies
  2. Verify Python version compatibility (3.8+)
  3. Check logs in Streamlit Cloud dashboard

### Slow Performance
- **Issue**: Simulation takes too long
- **Solutions**:
  1. Reduce number of simulations (try 1,000-5,000)
  2. Reduce rounds per game
  3. Streamlit Cloud has resource limits on free tier

---

## 🎯 Features of the Web App

### Interactive Controls
- 🎲 Adjustable simulation parameters via sidebar
- 💰 Configurable bankroll, bet amounts, rounds
- 🏠 Tweak house edge parameters in real-time
- 📊 Multiple betting strategies to test

### Real-Time Analysis
- 📈 Summary statistics comparison
- 📉 Interactive visualizations
- 🔬 Statistical hypothesis testing
- 💾 Download results as CSV

### Visualizations
1. **Profit Distributions** - Histogram, box plot, CDF, density
2. **House Profit** - Distribution and comparison charts
3. **Win/Loss Analysis** - Win rates, bankruptcy rates
4. **Cumulative Profit** - Long-term trend visualization

---

## 🌟 App Features

### User Experience
- Clean, intuitive interface
- Responsive design for mobile/tablet
- Real-time progress indicators
- Expandable help sections
- Custom color theme

### Performance
- Session state management (caching results)
- Efficient NumPy/Pandas operations
- Progress bars for long operations
- Background processing

### Educational Value
- Explains game rules clearly
- Shows theoretical calculations
- Compares fair vs. tweaked games
- Demonstrates Monte Carlo methods
- Statistical interpretation

---

## 📊 Using the App

### 1. Configure Simulation
Use the **sidebar** to set:
- Initial bankroll ($100-$10,000)
- Number of simulations (100-20,000)
- Rounds per game (10-500)
- Bet amount per round ($1-$100)
- Betting strategy (random, single color, house color)

### 2. Adjust House Edge
Modify the **tweak parameters**:
- House color (which color appears more often)
- House color probability (16.67%-30%)
- Payout modifier (80%-100%)

### 3. Run Simulation
- Click **"🚀 Run Simulation"** button
- Wait for progress bar to complete (10 sec - 2 min)
- View results automatically

### 4. Analyze Results
Explore multiple tabs:
- **Summary Statistics** - Key metrics comparison
- **Profit Distributions** - Visual comparison
- **House Profit** - Casino perspective
- **Win/Loss Analysis** - Player success rates
- **Statistical Tests** - Hypothesis testing

### 5. Download Data
Get results for further analysis:
- Fair game CSV
- Tweaked game CSV
- Analysis report TXT

---

## 🔐 Security Notes

- This app runs entirely client-side
- No data is collected or stored
- No authentication required
- No external API calls
- Safe for academic use

---

## 📱 Sharing Your App

Once deployed, you can:
- Share the URL with classmates/professors
- Embed in presentations
- Include in project reports
- Add to your portfolio

Example URL format:
```
https://YOUR_USERNAME-color-game-simulator.streamlit.app
```

---

## 🆘 Support

### Resources
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [GitHub Issues](https://github.com/YOUR_USERNAME/color-game-simulator/issues)

### Common Questions

**Q: Can I customize the colors?**  
A: Yes! Edit `.streamlit/config.toml` and change the `[theme]` section.

**Q: How many simulations can I run?**  
A: Locally, unlimited. On Streamlit Cloud, keep under 20,000 for performance.

**Q: Can I add more game types?**  
A: Yes! Extend the `ColorGame` class in `color_game.py` and update `app.py`.

**Q: Is this free?**  
A: Yes! Streamlit Community Cloud offers free hosting for public apps.

---

## 🎓 Academic Use

Perfect for:
- Modeling & Simulation courses
- Statistics projects
- Probability theory demonstrations
- Monte Carlo method tutorials
- Data science portfolios

### Citing This Project
```
Filipino Color Game Monte Carlo Simulator
Python implementation with Streamlit web interface
https://github.com/YOUR_USERNAME/color-game-simulator
December 2025
```

---

**Happy Simulating! 🎲📊**
