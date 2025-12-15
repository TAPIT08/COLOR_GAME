"""
Filipino Color Game - Interactive Web Application
==================================================
Play the game, run simulations, and learn about the Filipino "Perya" Color Game.

Author: Data Science Project
Date: December 2025
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from color_game import ColorGame, TweakedColorGame
from simulation import GameSimulator
from analysis import GameAnalyzer
from visualization import GameVisualizer

# Page configuration
st.set_page_config(
    page_title="Filipino Color Game",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ECDC4;
        font-weight: bold;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .dice {
        width: 120px;
        height: 120px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Color definitions
COLOR_CODES = {
    'Red': '#FF0000',
    'Blue': '#0000FF',
    'Yellow': '#FFD700',
    'White': '#FFFFFF',
    'Green': '#00FF00',
    'Pink': '#FF69B4'
}

COLORS = list(COLOR_CODES.keys())


def initialize_session_state():
    """Initialize all session state variables."""
    # Navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'Game'
    
    # Game state
    if 'game_instance' not in st.session_state:
        st.session_state.game_instance = None
    if 'dice_results' not in st.session_state:
        st.session_state.dice_results = None
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    
    # Simulation state
    if 'simulation_run' not in st.session_state:
        st.session_state.simulation_run = False
    if 'fair_results' not in st.session_state:
        st.session_state.fair_results = None
    if 'tweaked_results' not in st.session_state:
        st.session_state.tweaked_results = None


def get_dice_html(color):
    """Generate HTML for a dice."""
    bg_color = COLOR_CODES.get(color, '#888888')
    border_color = 'black' if color == 'White' else bg_color
    text_color = 'black' if color in ['White', 'Yellow'] else 'white'
    
    return f"""
    <div style="
        width: 120px;
        height: 120px;
        background-color: {bg_color};
        border: 3px solid {border_color};
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: bold;
        color: {text_color};
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin: 10px;
        text-align: center;
    ">
        {color}
    </div>
    """


# ============================================================================
# GAME MODE
# ============================================================================

def render_game_sidebar():
    """Sidebar for game mode."""
    st.sidebar.title("🎮 Game Settings")
    st.sidebar.markdown("---")
    
    # Game Configuration
    st.sidebar.subheader("⚙️ Game Configuration")
    
    initial_bankroll = st.sidebar.number_input(
        "💰 Starting Bankroll ($)",
        min_value=10,
        max_value=100000,
        value=1000,
        step=100
    )
    
    game_type = st.sidebar.radio(
        "🎲 Game Type",
        options=['Fair Game', 'Tweaked Game (House Edge)'],
        help="Fair: Equal probabilities. Tweaked: House advantage"
    )
    
    # Tweaked game settings
    house_color = 'Red'
    if game_type == 'Tweaked Game (House Edge)':
        st.sidebar.markdown("**House Edge Settings:**")
        house_color = st.sidebar.selectbox(
            "Favorite Color",
            options=COLORS,
            index=0
        )
    
    # New Game Button
    if st.sidebar.button("🔄 New Game", use_container_width=True, type="primary"):
        if game_type == 'Fair Game':
            st.session_state.game_instance = ColorGame(initial_bankroll=initial_bankroll)
        else:
            st.session_state.game_instance = TweakedColorGame(
                initial_bankroll=initial_bankroll,
                house_color=house_color,
                house_color_weight=0.20,
                payout_modifier=0.95
            )
        st.session_state.dice_results = None
        st.session_state.last_result = None
        st.success("🎮 New game started!")
    
    # Initialize game if doesn't exist
    if st.session_state.game_instance is None:
        if game_type == 'Fair Game':
            st.session_state.game_instance = ColorGame(initial_bankroll=initial_bankroll)
        else:
            st.session_state.game_instance = TweakedColorGame(
                initial_bankroll=initial_bankroll,
                house_color=house_color,
                house_color_weight=0.20,
                payout_modifier=0.95
            )
    
    st.sidebar.markdown("---")
    
    # Current Stats
    st.sidebar.subheader("📊 Your Stats")
    game = st.session_state.game_instance
    
    st.sidebar.metric("Current Bankroll", f"${game.player_bankroll:.2f}")
    profit = game.player_bankroll - game.initial_bankroll
    st.sidebar.metric("Profit/Loss", f"${profit:.2f}", delta=f"{profit:.2f}")
    st.sidebar.metric("Rounds Played", len(game.game_history))
    
    if len(game.game_history) > 0:
        wins = sum(1 for r in game.game_history if r['total_winnings'] > 0)
        st.sidebar.metric("Win Rate", f"{(wins/len(game.game_history)*100):.1f}%")
    
    st.sidebar.markdown("---")
    
    # Game Rules
    with st.sidebar.expander("📖 Game Rules"):
        st.markdown("""
        ### How to Play
        1. Enter bet amounts for colors (0 to skip)
        2. Click "🎲 Roll the Dice!"
        3. Win based on matches:
           - **0 matches**: Lose bets
           - **1 match**: Win 1× bet
           - **2 matches**: Win 2× bet
           - **3 matches**: Win 3× bet
        
        ### Payouts Example ($10 bet)
        - 1 match: +$10 (total $20)
        - 2 matches: +$20 (total $30)
        - 3 matches: +$30 (total $40)
        """)


def render_game_page():
    """Main game page."""
    st.markdown('<div class="main-header">🎲 Play Color Game</div>', unsafe_allow_html=True)
    
    game = st.session_state.game_instance
    
    # Check if bankrupt
    if game.player_bankroll <= 0:
        st.error("💔 **BANKRUPT!** You've run out of money. Start a new game!")
        return
    
    # Display dice results
    st.markdown('<div class="sub-header">🎲 The Dice</div>', unsafe_allow_html=True)
    
    if st.session_state.dice_results is None:
        # Show placeholder dice
        cols = st.columns([1, 1, 1, 1, 1])
        with cols[1]:
            st.markdown(get_dice_html('❓'), unsafe_allow_html=True)
        with cols[2]:
            st.markdown(get_dice_html('❓'), unsafe_allow_html=True)
        with cols[3]:
            st.markdown(get_dice_html('❓'), unsafe_allow_html=True)
        st.info("👆 Place your bets below, then roll the dice!")
    else:
        # Show actual results
        dice = st.session_state.dice_results
        cols = st.columns([1, 1, 1, 1, 1])
        with cols[1]:
            st.markdown(get_dice_html(dice[0]), unsafe_allow_html=True)
        with cols[2]:
            st.markdown(get_dice_html(dice[1]), unsafe_allow_html=True)
        with cols[3]:
            st.markdown(get_dice_html(dice[2]), unsafe_allow_html=True)
    
    # Show last result
    if st.session_state.last_result is not None:
        result = st.session_state.last_result
        
        if result['total_winnings'] > 0:
            st.success(f"🎉 **YOU WON ${result['total_winnings']:.2f}!**")
        elif result['total_winnings'] < 0:
            st.error(f"😢 **You lost ${-result['total_winnings']:.2f}**")
        else:
            st.info("➖ **Break even!**")
        
        # Show breakdown
        with st.expander("📊 Round Details"):
            for color, data in result['bets'].items():
                if data['bet'] > 0:
                    st.write(f"**{color}**: Bet ${data['bet']:.2f} | Matches: {data['matches']} | Won: ${data['winnings']:.2f}")
    
    st.markdown("---")
    
    # Betting Interface
    st.markdown('<div class="sub-header">💰 Place Your Bets</div>', unsafe_allow_html=True)
    
    st.info(f"💵 **Available to bet**: ${game.player_bankroll:.2f}")
    
    # Create betting inputs
    cols = st.columns(3)
    bets = {}
    
    for idx, color in enumerate(COLORS):
        col_idx = idx % 3
        with cols[col_idx]:
            bg_color = COLOR_CODES[color]
            text_color = 'black' if color in ['White', 'Yellow'] else 'white'
            
            st.markdown(f"""
            <div style="
                background-color: {bg_color};
                color: {text_color};
                padding: 10px;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                margin-bottom: 10px;
                border: 2px solid {'black' if color == 'White' else bg_color};
            ">
                {color}
            </div>
            """, unsafe_allow_html=True)
            
            bets[color] = st.number_input(
                f"Bet on {color}",
                min_value=0.0,
                max_value=float(game.player_bankroll),
                value=0.0,
                step=1.0,
                key=f"bet_{color}",
                label_visibility="collapsed"
            )
    
    # Calculate total bet
    total_bet = sum(bets.values())
    
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col2:
        st.metric("Total Bet", f"${total_bet:.2f}")
    
    st.markdown("---")
    
    # Roll button
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        roll_button = st.button(
            "🎲 ROLL THE DICE!",
            use_container_width=True,
            type="primary",
            disabled=(total_bet <= 0 or total_bet > game.player_bankroll)
        )
    
    if roll_button and total_bet > 0:
        # Roll the dice
        dice_results = game.roll_dice()
        st.session_state.dice_results = dice_results
        
        # Process each bet
        total_winnings = 0
        bet_details = {}
        
        for color, bet_amount in bets.items():
            if bet_amount > 0:
                matches = dice_results.count(color)
                winnings, _ = game.calculate_payout(color, dice_results, bet_amount)
                total_winnings += winnings
                
                bet_details[color] = {
                    'bet': bet_amount,
                    'matches': matches,
                    'winnings': winnings
                }
        
        # Update bankroll
        game.player_bankroll += total_winnings
        game.house_profit -= total_winnings
        
        # Record in history
        game.game_history.append({
            'dice_results': dice_results,
            'total_bet': total_bet,
            'total_winnings': total_winnings,
            'player_bankroll': game.player_bankroll
        })
        
        # Store result
        st.session_state.last_result = {
            'total_winnings': total_winnings,
            'bets': bet_details,
            'dice': dice_results
        }
        
        st.rerun()
    
    # Game History
    if len(game.game_history) > 0:
        st.markdown("---")
        st.markdown('<div class="sub-header">📜 Game History</div>', unsafe_allow_html=True)
        
        history_df = pd.DataFrame([
            {
                'Round': i + 1,
                'Dice': ', '.join(h['dice_results']),
                'Bet': f"${h['total_bet']:.2f}",
                'Result': f"${h['total_winnings']:.2f}",
                'Bankroll': f"${h['player_bankroll']:.2f}"
            }
            for i, h in enumerate(game.game_history[-10:])  # Last 10 rounds
        ])
        
        st.dataframe(history_df, use_container_width=True, hide_index=True)


# ============================================================================
# SIMULATION MODE
# ============================================================================

def render_simulation_sidebar():
    """Sidebar for simulation mode."""
    st.sidebar.title("🔬 Simulation Settings")
    st.sidebar.markdown("---")
    
    # Quick presets
    st.sidebar.subheader("🚀 Quick Presets")
    preset = st.sidebar.selectbox(
        "Choose a preset",
        options=['Custom', 'Quick Test (1K)', 'Standard (10K)', 'Deep Analysis (20K)']
    )
    
    if preset == 'Quick Test (1K)':
        num_simulations = 1000
        rounds_per_game = 50
    elif preset == 'Standard (10K)':
        num_simulations = 10000
        rounds_per_game = 100
    elif preset == 'Deep Analysis (20K)':
        num_simulations = 20000
        rounds_per_game = 150
    else:
        num_simulations = st.sidebar.select_slider(
            "Number of Simulations",
            options=[100, 500, 1000, 5000, 10000, 20000],
            value=10000
        )
        rounds_per_game = st.sidebar.slider(
            "Rounds per Game",
            min_value=10,
            max_value=500,
            value=100,
            step=10
        )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Parameters")
    
    initial_bankroll = st.sidebar.number_input(
        "Initial Bankroll ($)",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100
    )
    
    bet_amount = st.sidebar.number_input(
        "Bet Amount per Round ($)",
        min_value=1,
        max_value=100,
        value=10,
        step=1
    )
    
    betting_strategy = st.sidebar.selectbox(
        "Betting Strategy",
        options=['random', 'single_color', 'house_color'],
        format_func=lambda x: {
            'random': '🎲 Random Colors',
            'single_color': '🔴 Always Red',
            'house_color': '🏠 House Color'
        }[x]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🏠 House Edge Tweaks")
    
    house_color = st.sidebar.selectbox(
        "House Color",
        options=COLORS,
        index=0
    )
    
    house_color_weight = st.sidebar.slider(
        "House Color Probability (%)",
        min_value=16.67,
        max_value=30.0,
        value=20.0,
        step=0.1,
        format="%.2f%%"
    ) / 100
    
    payout_modifier = st.sidebar.slider(
        "Payout Modifier (%)",
        min_value=80,
        max_value=100,
        value=95,
        step=1
    ) / 100
    
    return {
        'initial_bankroll': initial_bankroll,
        'num_simulations': num_simulations,
        'rounds_per_game': rounds_per_game,
        'bet_amount': bet_amount,
        'betting_strategy': betting_strategy,
        'house_color': house_color,
        'house_color_weight': house_color_weight,
        'payout_modifier': payout_modifier
    }


def render_simulation_page(params):
    """Main simulation page."""
    st.markdown('<div class="main-header">🔬 Monte Carlo Simulation</div>', unsafe_allow_html=True)
    
    st.markdown("""
    Run thousands of simulations to analyze the statistical properties of the Color Game.
    Compare fair game vs. tweaked game with house edge.
    """)
    
    # Theoretical analysis
    st.markdown("---")
    st.markdown("### 📊 Theoretical Analysis")
    
    fair_game = ColorGame(initial_bankroll=params['initial_bankroll'])
    tweaked_game = TweakedColorGame(
        initial_bankroll=params['initial_bankroll'],
        house_color=params['house_color'],
        house_color_weight=params['house_color_weight'],
        payout_modifier=params['payout_modifier']
    )
    
    fair_edge = fair_game.get_theoretical_house_edge()
    tweaked_edge = tweaked_game.get_theoretical_house_edge()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Fair Game House Edge", f"{fair_edge:.4%}")
    with col2:
        st.metric("Tweaked Game House Edge", f"{tweaked_edge:.4%}", 
                 delta=f"+{(tweaked_edge - fair_edge):.4%}", delta_color="inverse")
    with col3:
        st.metric("House Edge Increase", f"{(tweaked_edge - fair_edge):.4%}")
    
    st.markdown("---")
    
    # Run simulation button
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Run Simulation", use_container_width=True, type="primary"):
            with st.spinner("Running Monte Carlo simulation..."):
                # Set seed
                np.random.seed(42)
                
                # Progress
                progress_bar = st.progress(0, text="Initializing...")
                
                # Fair game
                progress_bar.progress(20, text="Simulating fair game...")
                fair_simulator = GameSimulator(fair_game)
                fair_results = fair_simulator.run_simulation(
                    num_simulations=params['num_simulations'],
                    rounds_per_game=params['rounds_per_game'],
                    bet_amount=params['bet_amount'],
                    strategy=params['betting_strategy'],
                    show_progress=False
                )
                
                # Tweaked game
                progress_bar.progress(60, text="Simulating tweaked game...")
                tweaked_simulator = GameSimulator(tweaked_game)
                tweaked_results = tweaked_simulator.run_simulation(
                    num_simulations=params['num_simulations'],
                    rounds_per_game=params['rounds_per_game'],
                    bet_amount=params['bet_amount'],
                    strategy=params['betting_strategy'],
                    show_progress=False
                )
                
                # Analysis
                progress_bar.progress(90, text="Analyzing results...")
                analyzer = GameAnalyzer(fair_results, tweaked_results)
                visualizer = GameVisualizer(fair_results, tweaked_results)
                
                # Store in session state
                st.session_state.fair_results = fair_results
                st.session_state.tweaked_results = tweaked_results
                st.session_state.analyzer = analyzer
                st.session_state.visualizer = visualizer
                st.session_state.simulation_run = True
                
                progress_bar.progress(100, text="Complete!")
                progress_bar.empty()
                
            st.success(f"✅ Completed {params['num_simulations'] * 2:,} simulations!")
            st.rerun()
    
    # Display results if simulation run
    if st.session_state.simulation_run:
        st.markdown("---")
        st.markdown("### 📈 Summary Statistics")
        
        stats = st.session_state.analyzer.calculate_summary_statistics()
        house_edge = st.session_state.analyzer.calculate_house_edge()
        
        # Metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Fair Game**")
            st.metric("Mean Profit", f"${stats['fair']['mean_profit']:.2f}")
            st.metric("Win Rate", f"{stats['fair']['win_rate']:.2%}")
            st.metric("House Edge (Empirical)", f"{house_edge['fair']:.4%}")
        
        with col2:
            st.markdown("**Tweaked Game**")
            st.metric("Mean Profit", f"${stats['tweaked']['mean_profit']:.2f}",
                     delta=f"${stats['tweaked']['mean_profit'] - stats['fair']['mean_profit']:.2f}")
            st.metric("Win Rate", f"{stats['tweaked']['win_rate']:.2%}",
                     delta=f"{(stats['tweaked']['win_rate'] - stats['fair']['win_rate'])*100:.1f}pp")
            st.metric("House Edge (Empirical)", f"{house_edge['tweaked']:.4%}",
                     delta=f"+{house_edge['difference']:.4%}", delta_color="inverse")
        
        # Visualizations
        st.markdown("---")
        st.markdown("### 📊 Visualizations")
        
        tab1, tab2, tab3 = st.tabs(["Profit Distributions", "House Profit", "Win/Loss"])
        
        with tab1:
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            
            # Histogram
            axes[0].hist(st.session_state.fair_results['net_profit'], bins=50, alpha=0.6, label='Fair', color='blue')
            axes[0].hist(st.session_state.tweaked_results['net_profit'], bins=50, alpha=0.6, label='Tweaked', color='red')
            axes[0].set_xlabel('Net Profit ($)')
            axes[0].set_ylabel('Frequency')
            axes[0].set_title('Profit Distribution')
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)
            
            # Box plot
            bp = axes[1].boxplot([st.session_state.fair_results['net_profit'], 
                                  st.session_state.tweaked_results['net_profit']],
                                 labels=['Fair', 'Tweaked'], patch_artist=True)
            bp['boxes'][0].set_facecolor('lightblue')
            bp['boxes'][1].set_facecolor('lightcoral')
            axes[1].set_ylabel('Net Profit ($)')
            axes[1].set_title('Box Plot Comparison')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
        
        with tab2:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            fair_house = [st.session_state.fair_results['house_profit'].mean()]
            tweaked_house = [st.session_state.tweaked_results['house_profit'].mean()]
            
            x = ['Fair Game', 'Tweaked Game']
            y = [fair_house[0], tweaked_house[0]]
            colors = ['green', 'darkred']
            
            ax.bar(x, y, color=colors, alpha=0.7, edgecolor='black')
            ax.set_ylabel('Average House Profit ($)')
            ax.set_title('House Profit Comparison')
            ax.grid(True, alpha=0.3, axis='y')
            
            for i, v in enumerate(y):
                ax.text(i, v + 5, f'${v:.2f}', ha='center', fontweight='bold')
            
            st.pyplot(fig)
            plt.close()
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Fair Game Win Rates**")
                fair_wins = (st.session_state.fair_results['net_profit'] > 0).sum()
                fair_losses = (st.session_state.fair_results['net_profit'] <= 0).sum()
                
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie([fair_wins, fair_losses], labels=['Wins', 'Losses'],
                       colors=['lightgreen', 'lightcoral'], autopct='%1.1f%%', startangle=90)
                ax.set_title('Fair Game Win/Loss')
                st.pyplot(fig)
                plt.close()
            
            with col2:
                st.markdown("**Tweaked Game Win Rates**")
                tweaked_wins = (st.session_state.tweaked_results['net_profit'] > 0).sum()
                tweaked_losses = (st.session_state.tweaked_results['net_profit'] <= 0).sum()
                
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie([tweaked_wins, tweaked_losses], labels=['Wins', 'Losses'],
                       colors=['lightgreen', 'lightcoral'], autopct='%1.1f%%', startangle=90)
                ax.set_title('Tweaked Game Win/Loss')
                st.pyplot(fig)
                plt.close()
        
        # Download section
        st.markdown("---")
        st.markdown("### 💾 Download Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fair_csv = st.session_state.fair_results.to_csv(index=False)
            st.download_button(
                label="📥 Fair Game Data",
                data=fair_csv,
                file_name="fair_game_results.csv",
                mime="text/csv"
            )
        
        with col2:
            tweaked_csv = st.session_state.tweaked_results.to_csv(index=False)
            st.download_button(
                label="📥 Tweaked Game Data",
                data=tweaked_csv,
                file_name="tweaked_game_results.csv",
                mime="text/csv"
            )
        
        with col3:
            report = f"""Simulation Report
            
Fair Game: ${stats['fair']['mean_profit']:.2f} mean profit
Tweaked Game: ${stats['tweaked']['mean_profit']:.2f} mean profit
House Edge Difference: {house_edge['difference']:.4%}
"""
            st.download_button(
                label="📥 Analysis Report",
                data=report,
                file_name="simulation_report.txt",
                mime="text/plain"
            )


# ============================================================================
# ABOUT MODE
# ============================================================================

def render_about_sidebar():
    """Sidebar for about mode."""
    st.sidebar.title("ℹ️ About")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("""
    ### 🎲 Color Game
    
    A Filipino carnival (perya) game demonstrating probability theory and Monte Carlo simulation.
    
    ### 📚 Project Info
    
    **Purpose**: Educational  
    **Course**: Modeling & Simulation  
    **Date**: December 2025
    
    ### 🛠️ Technologies
    
    - Python 3.11+
    - Streamlit
    - NumPy & Pandas
    - Matplotlib & Seaborn
    - SciPy
    
    ### ⚠️ Disclaimer
    
    For educational purposes only.  
    Not for actual gambling.
    """)


def render_about_page():
    """Main about page."""
    st.markdown('<div class="main-header">ℹ️ About the Color Game</div>', unsafe_allow_html=True)
    
    # Game Description
    st.markdown("## 🎲 What is the Color Game?")
    
    st.markdown("""
    The **Filipino Color Game** (also known as "Color Wheel" or "Perya Game") is a traditional 
    carnival game popular in the Philippines. It's a simple betting game based on probability 
    and chance, making it perfect for demonstrating statistical concepts.
    """)
    
    # How it works
    st.markdown("## 🎮 How It Works")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Game Mechanics
        
        1. **Six Colors**: Red, Blue, Yellow, White, Green, Pink
        2. **Three Dice**: Each die has all six colors
        3. **Place Bets**: Choose colors to bet on
        4. **Roll Dice**: All three dice rolled simultaneously
        5. **Count Matches**: Win based on how many dice match your color
        """)
    
    with col2:
        st.markdown("""
        ### Payout Structure
        
        For a $10 bet on a color:
        
        - **0 matches**: LOSE $10
        - **1 match**: WIN $10 (get $20 total)
        - **2 matches**: WIN $20 (get $30 total)
        - **3 matches**: WIN $30 (get $40 total)
        """)
    
    # Mathematics
    st.markdown("---")
    st.markdown("## 📊 The Mathematics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Fair Game Probabilities
        
        When all colors have equal probability (1/6):
        
        ```
        P(0 matches) = (5/6)³ = 57.87%
        P(1 match)   = 3×(1/6)×(5/6)² = 34.72%
        P(2 matches) = 3×(1/6)²×(5/6) = 6.94%
        P(3 matches) = (1/6)³ = 0.46%
        ```
        
        **Expected Value per $1 bet**: -$0.0787  
        **House Edge**: 7.87%
        """)
    
    with col2:
        st.markdown("""
        ### Tweaked Game
        
        With house advantage:
        
        - House color appears **20%** of the time
        - Other colors: **16%** each
        - Payouts reduced to **95%**
        
        **Result**: House edge increases to ~11-13%
        
        This means **$33.64 more loss** per 100 games on average!
        """)
    
    # Simulation
    st.markdown("---")
    st.markdown("## 🔬 Monte Carlo Simulation")
    
    st.markdown("""
    This project uses **Monte Carlo simulation** to:
    
    - Run thousands of game sessions
    - Calculate empirical probabilities
    - Validate theoretical predictions
    - Compare fair vs. tweaked games
    - Demonstrate long-term outcomes
    
    ### Why Simulation?
    
    1. **Approximate Complex Probabilities**: Some outcomes are hard to calculate analytically
    2. **Visualize Long-term Behavior**: See what happens over many games
    3. **Test Strategies**: Compare different betting approaches
    4. **Educational Value**: Learn through experimentation
    """)
    
    # Learning Objectives
    st.markdown("---")
    st.markdown("## 🎓 Learning Objectives")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Probability Theory**
        - Discrete distributions
        - Expected value
        - Law of large numbers
        - Binomial probabilities
        """)
    
    with col2:
        st.markdown("""
        **Monte Carlo Methods**
        - Random sampling
        - Variance reduction
        - Convergence analysis
        - Statistical validation
        """)
    
    with col3:
        st.markdown("""
        **Data Science**
        - Statistical analysis
        - Hypothesis testing
        - Data visualization
        - Python programming
        """)
    
    # House Edge
    st.markdown("---")
    st.markdown("## 🏠 Understanding House Edge")
    
    st.info("""
    💡 **Key Insight**: Even in the "fair" game, the house has a mathematical advantage!
    
    The house edge ensures that over many games, the casino (house) will always profit. 
    This is achieved through:
    
    1. **Payout structure** that doesn't fully compensate for probabilities
    2. **Weighted probabilities** (in tweaked version)
    3. **Long-term statistics** that favor the house
    
    **Remember**: In gambling, "the house always wins" in the long run!
    """)
    
    # How to Use
    st.markdown("---")
    st.markdown("## 📱 How to Use This App")
    
    tab1, tab2, tab3 = st.tabs(["🎮 Game Mode", "🔬 Simulation Mode", "📚 Tips"])
    
    with tab1:
        st.markdown("""
        ### Playing the Game
        
        1. **Set your bankroll** in the sidebar
        2. **Choose game type**: Fair or Tweaked
        3. **Place bets** on colors (can bet on multiple)
        4. **Click "Roll the Dice!"**
        5. **Watch results** and see your winnings
        6. **Track statistics** in the sidebar
        
        Try to beat the house edge! (Hint: You can't in the long run 😉)
        """)
    
    with tab2:
        st.markdown("""
        ### Running Simulations
        
        1. **Choose a preset** or customize parameters
        2. **Adjust house edge** settings
        3. **Click "Run Simulation"**
        4. **Analyze results** in various charts
        5. **Download data** for further analysis
        
        Compare how fair and tweaked games differ over thousands of trials!
        """)
    
    with tab3:
        st.markdown("""
        ### Pro Tips
        
        - **Start with Game Mode** to understand mechanics
        - **Run Quick Test (1K)** first to see patterns
        - **Compare both game types** side-by-side
        - **Check win rates** - they're always < 50%!
        - **Download data** for Excel analysis
        - **Try different strategies** in simulation mode
        
        ### Educational Use
        
        This project is perfect for:
        - Probability & Statistics courses
        - Modeling & Simulation classes
        - Data Science demonstrations
        - Monte Carlo method tutorials
        - Python programming practice
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 20px;'>
        <p><strong>🎲 Filipino Color Game Simulator</strong></p>
        <p>Educational Project | December 2025</p>
        <p><em>"The house always wins... but now you understand why!"</em></p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    initialize_session_state()
    
    # Navigation
    st.sidebar.title("🎯 Navigation")
    
    page = st.sidebar.radio(
        "Choose Mode:",
        options=['Game', 'Simulation', 'About'],
        format_func=lambda x: {
            'Game': '🎮 Play Game',
            'Simulation': '🔬 Run Simulations',
            'About': 'ℹ️ About & Help'
        }[x],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    # Render appropriate page
    if page == 'Game':
        render_game_sidebar()
        render_game_page()
    elif page == 'Simulation':
        params = render_simulation_sidebar()
        render_simulation_page(params)
    else:  # About
        render_about_sidebar()
        render_about_page()


if __name__ == "__main__":
    main()
