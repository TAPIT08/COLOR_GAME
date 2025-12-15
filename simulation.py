"""
Monte Carlo Simulation Module
------------------------------
This module handles running multiple simulations of the Color Game.
"""

import numpy as np
import pandas as pd
from typing import List, Dict
from color_game import ColorGame, TweakedColorGame
from tqdm import tqdm


class GameSimulator:
    """
    Simulator for running multiple games and collecting statistics.
    """
    
    def __init__(self, game_model: ColorGame):
        """
        Initialize the simulator.
        
        Args:
            game_model: Instance of ColorGame or TweakedColorGame
        """
        self.game_model = game_model
        self.simulation_results = []
    
    def run_single_game(self, num_rounds: int, bet_amount: float, strategy: str = 'random') -> Dict:
        """
        Run a single game session with multiple rounds.
        
        Args:
            num_rounds: Number of rounds to play
            bet_amount: Amount to bet each round
            strategy: Betting strategy ('random', 'single_color', 'house_color')
            
        Returns:
            Dictionary with game session results
        """
        self.game_model.reset()
        
        for _ in range(num_rounds):
            # Choose betting strategy
            if strategy == 'random':
                bet_color = np.random.choice(self.game_model.COLORS)
            elif strategy == 'single_color':
                bet_color = 'Red'  # Always bet on Red
            elif strategy == 'house_color' and isinstance(self.game_model, TweakedColorGame):
                bet_color = self.game_model.house_color
            else:
                bet_color = np.random.choice(self.game_model.COLORS)
            
            # Stop if player runs out of money
            if self.game_model.player_bankroll < bet_amount:
                break
            
            self.game_model.play_round(bet_color, bet_amount)
        
        # Calculate session statistics
        return {
            'initial_bankroll': self.game_model.initial_bankroll,
            'final_bankroll': self.game_model.player_bankroll,
            'net_profit': self.game_model.player_bankroll - self.game_model.initial_bankroll,
            'house_profit': self.game_model.house_profit,
            'rounds_played': len(self.game_model.game_history),
            'wins': sum(1 for r in self.game_model.game_history if r['net_winnings'] > 0),
            'losses': sum(1 for r in self.game_model.game_history if r['net_winnings'] < 0),
            'total_wagered': sum(r['bet_amount'] for r in self.game_model.game_history),
        }
    
    def run_simulation(self, num_simulations: int, rounds_per_game: int, 
                       bet_amount: float, strategy: str = 'random',
                       show_progress: bool = True) -> pd.DataFrame:
        """
        Run Monte Carlo simulation with multiple game sessions.
        
        Args:
            num_simulations: Number of game sessions to simulate
            rounds_per_game: Number of rounds in each game session
            bet_amount: Amount to bet each round
            strategy: Betting strategy to use
            show_progress: Whether to show progress bar
            
        Returns:
            DataFrame with simulation results
        """
        results = []
        
        iterator = tqdm(range(num_simulations), desc="Running simulations") if show_progress else range(num_simulations)
        
        for sim_id in iterator:
            session_result = self.run_single_game(rounds_per_game, bet_amount, strategy)
            session_result['simulation_id'] = sim_id
            results.append(session_result)
        
        self.simulation_results = pd.DataFrame(results)
        return self.simulation_results
    
    def get_detailed_round_data(self, num_games: int, rounds_per_game: int, 
                                bet_amount: float, strategy: str = 'random') -> pd.DataFrame:
        """
        Get detailed data for each round across multiple games.
        
        Args:
            num_games: Number of games to run
            rounds_per_game: Rounds per game
            bet_amount: Bet amount per round
            strategy: Betting strategy
            
        Returns:
            DataFrame with all round-level data
        """
        all_rounds = []
        
        for game_id in tqdm(range(num_games), desc="Collecting detailed data"):
            self.game_model.reset()
            
            for round_num in range(rounds_per_game):
                if strategy == 'random':
                    bet_color = np.random.choice(self.game_model.COLORS)
                elif strategy == 'single_color':
                    bet_color = 'Red'
                elif strategy == 'house_color' and isinstance(self.game_model, TweakedColorGame):
                    bet_color = self.game_model.house_color
                else:
                    bet_color = np.random.choice(self.game_model.COLORS)
                
                if self.game_model.player_bankroll < bet_amount:
                    break
                
                round_result = self.game_model.play_round(bet_color, bet_amount)
                round_result['game_id'] = game_id
                round_result['round_num'] = round_num
                all_rounds.append(round_result)
        
        return pd.DataFrame(all_rounds)


def compare_models(fair_game: ColorGame, tweaked_game: TweakedColorGame,
                   num_simulations: int = 10000, rounds_per_game: int = 100,
                   bet_amount: float = 10.0, strategy: str = 'random') -> Dict[str, pd.DataFrame]:
    """
    Run simulations for both fair and tweaked games for comparison.
    
    Args:
        fair_game: Fair ColorGame instance
        tweaked_game: TweakedColorGame instance
        num_simulations: Number of simulations for each model
        rounds_per_game: Rounds per game session
        bet_amount: Bet amount per round
        strategy: Betting strategy
        
    Returns:
        Dictionary with 'fair' and 'tweaked' DataFrames
    """
    print("=" * 80)
    print("MONTE CARLO SIMULATION: Color Game Analysis")
    print("=" * 80)
    
    # Simulate fair game
    print("\n1. Running FAIR GAME simulations...")
    fair_simulator = GameSimulator(fair_game)
    fair_results = fair_simulator.run_simulation(num_simulations, rounds_per_game, bet_amount, strategy)
    
    # Simulate tweaked game
    print("\n2. Running TWEAKED GAME simulations...")
    tweaked_simulator = GameSimulator(tweaked_game)
    tweaked_results = tweaked_simulator.run_simulation(num_simulations, rounds_per_game, bet_amount, strategy)
    
    print("\n✓ Simulations complete!")
    print(f"  - Total simulations: {num_simulations * 2}")
    print(f"  - Rounds per game: {rounds_per_game}")
    print(f"  - Bet amount: ${bet_amount}")
    print(f"  - Strategy: {strategy}")
    
    return {
        'fair': fair_results,
        'tweaked': tweaked_results
    }
