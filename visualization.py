"""
Visualization Module
--------------------
Creates plots and charts for analyzing game simulation results.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10


class GameVisualizer:
    """
    Creates visualizations for game analysis.
    """
    
    def __init__(self, fair_results: pd.DataFrame, tweaked_results: pd.DataFrame):
        """
        Initialize visualizer with simulation results.
        
        Args:
            fair_results: DataFrame from fair game simulations
            tweaked_results: DataFrame from tweaked game simulations
        """
        self.fair_results = fair_results
        self.tweaked_results = tweaked_results
    
    def plot_profit_distributions(self, save_path: str = None):
        """
        Plot profit distribution comparison between fair and tweaked games.
        
        Args:
            save_path: Optional path to save the figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Histogram comparison
        axes[0, 0].hist(self.fair_results['net_profit'], bins=50, alpha=0.6, 
                       label='Fair Game', color='blue', edgecolor='black')
        axes[0, 0].hist(self.tweaked_results['net_profit'], bins=50, alpha=0.6, 
                       label='Tweaked Game', color='red', edgecolor='black')
        axes[0, 0].axvline(self.fair_results['net_profit'].mean(), color='blue', 
                          linestyle='--', linewidth=2, label='Fair Mean')
        axes[0, 0].axvline(self.tweaked_results['net_profit'].mean(), color='red', 
                          linestyle='--', linewidth=2, label='Tweaked Mean')
        axes[0, 0].set_xlabel('Net Profit ($)')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Profit Distribution Comparison')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Box plot comparison
        data_to_plot = [self.fair_results['net_profit'], self.tweaked_results['net_profit']]
        bp = axes[0, 1].boxplot(data_to_plot, labels=['Fair Game', 'Tweaked Game'],
                                patch_artist=True, showmeans=True)
        bp['boxes'][0].set_facecolor('lightblue')
        bp['boxes'][1].set_facecolor('lightcoral')
        axes[0, 1].set_ylabel('Net Profit ($)')
        axes[0, 1].set_title('Profit Distribution Box Plot')
        axes[0, 1].grid(True, alpha=0.3)
        axes[0, 1].axhline(0, color='black', linestyle='-', linewidth=1)
        
        # 3. Cumulative distribution
        fair_sorted = np.sort(self.fair_results['net_profit'])
        tweaked_sorted = np.sort(self.tweaked_results['net_profit'])
        fair_cdf = np.arange(1, len(fair_sorted) + 1) / len(fair_sorted)
        tweaked_cdf = np.arange(1, len(tweaked_sorted) + 1) / len(tweaked_sorted)
        
        axes[1, 0].plot(fair_sorted, fair_cdf, label='Fair Game', color='blue', linewidth=2)
        axes[1, 0].plot(tweaked_sorted, tweaked_cdf, label='Tweaked Game', color='red', linewidth=2)
        axes[1, 0].set_xlabel('Net Profit ($)')
        axes[1, 0].set_ylabel('Cumulative Probability')
        axes[1, 0].set_title('Cumulative Distribution Function (CDF)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        axes[1, 0].axvline(0, color='black', linestyle='--', linewidth=1)
        
        # 4. Density plot
        self.fair_results['net_profit'].plot(kind='density', ax=axes[1, 1], 
                                              label='Fair Game', color='blue', linewidth=2)
        self.tweaked_results['net_profit'].plot(kind='density', ax=axes[1, 1], 
                                                label='Tweaked Game', color='red', linewidth=2)
        axes[1, 1].set_xlabel('Net Profit ($)')
        axes[1, 1].set_ylabel('Density')
        axes[1, 1].set_title('Profit Density Plot')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        axes[1, 1].axvline(0, color='black', linestyle='--', linewidth=1)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved profit distribution plot to {save_path}")
        
        plt.show()
    
    def plot_house_profit(self, save_path: str = None):
        """
        Plot house profit comparison.
        
        Args:
            save_path: Optional path to save the figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # 1. House profit distribution
        axes[0].hist(self.fair_results['house_profit'], bins=50, alpha=0.6, 
                    label='Fair Game', color='green', edgecolor='black')
        axes[0].hist(self.tweaked_results['house_profit'], bins=50, alpha=0.6, 
                    label='Tweaked Game', color='darkred', edgecolor='black')
        axes[0].axvline(self.fair_results['house_profit'].mean(), color='green', 
                       linestyle='--', linewidth=2, label='Fair Mean')
        axes[0].axvline(self.tweaked_results['house_profit'].mean(), color='darkred', 
                       linestyle='--', linewidth=2, label='Tweaked Mean')
        axes[0].set_xlabel('House Profit ($)')
        axes[0].set_ylabel('Frequency')
        axes[0].set_title('House Profit Distribution')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # 2. Cumulative house profit
        fair_cumsum = self.fair_results['house_profit'].cumsum()
        tweaked_cumsum = self.tweaked_results['house_profit'].cumsum()
        
        axes[1].plot(fair_cumsum.values, label='Fair Game', color='green', linewidth=2)
        axes[1].plot(tweaked_cumsum.values, label='Tweaked Game', color='darkred', linewidth=2)
        axes[1].set_xlabel('Number of Simulations')
        axes[1].set_ylabel('Cumulative House Profit ($)')
        axes[1].set_title('Cumulative House Profit Over Simulations')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Add summary text
        fair_total = self.fair_results['house_profit'].sum()
        tweaked_total = self.tweaked_results['house_profit'].sum()
        axes[1].text(0.05, 0.95, 
                    f'Fair Total: ${fair_total:,.2f}\nTweaked Total: ${tweaked_total:,.2f}\nDifference: ${tweaked_total - fair_total:,.2f}',
                    transform=axes[1].transAxes, verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved house profit plot to {save_path}")
        
        plt.show()
    
    def plot_win_loss_analysis(self, save_path: str = None):
        """
        Plot win/loss rate analysis.
        
        Args:
            save_path: Optional path to save the figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Calculate win rates
        fair_win_rate = (self.fair_results['net_profit'] > 0).mean()
        tweaked_win_rate = (self.tweaked_results['net_profit'] > 0).mean()
        
        # 1. Win rate bar chart
        win_rates = [fair_win_rate, tweaked_win_rate]
        loss_rates = [1 - fair_win_rate, 1 - tweaked_win_rate]
        
        x = np.arange(2)
        width = 0.35
        
        axes[0, 0].bar(x, win_rates, width, label='Win Rate', color='green', alpha=0.7)
        axes[0, 0].bar(x, loss_rates, width, bottom=win_rates, label='Loss Rate', color='red', alpha=0.7)
        axes[0, 0].set_ylabel('Rate')
        axes[0, 0].set_title('Win/Loss Rate Comparison')
        axes[0, 0].set_xticks(x)
        axes[0, 0].set_xticklabels(['Fair Game', 'Tweaked Game'])
        axes[0, 0].legend()
        axes[0, 0].set_ylim([0, 1])
        
        # Add percentage labels
        for i, (wr, lr) in enumerate(zip(win_rates, loss_rates)):
            axes[0, 0].text(i, wr/2, f'{wr:.1%}', ha='center', va='center', fontweight='bold')
            axes[0, 0].text(i, wr + lr/2, f'{lr:.1%}', ha='center', va='center', fontweight='bold')
        
        # 2. Average wins and losses
        fair_avg_wins = self.fair_results['wins'].mean()
        fair_avg_losses = self.fair_results['losses'].mean()
        tweaked_avg_wins = self.tweaked_results['wins'].mean()
        tweaked_avg_losses = self.tweaked_results['losses'].mean()
        
        x = np.arange(2)
        axes[0, 1].bar(x - width/2, [fair_avg_wins, tweaked_avg_wins], width, 
                      label='Avg Wins', color='green', alpha=0.7)
        axes[0, 1].bar(x + width/2, [fair_avg_losses, tweaked_avg_losses], width, 
                      label='Avg Losses', color='red', alpha=0.7)
        axes[0, 1].set_ylabel('Average Count')
        axes[0, 1].set_title('Average Wins and Losses per Game')
        axes[0, 1].set_xticks(x)
        axes[0, 1].set_xticklabels(['Fair Game', 'Tweaked Game'])
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # 3. Win/Loss ratio distribution
        fair_wl_ratio = self.fair_results['wins'] / (self.fair_results['losses'] + 1)
        tweaked_wl_ratio = self.tweaked_results['wins'] / (self.tweaked_results['losses'] + 1)
        
        axes[1, 0].hist(fair_wl_ratio, bins=30, alpha=0.6, label='Fair Game', 
                       color='blue', edgecolor='black')
        axes[1, 0].hist(tweaked_wl_ratio, bins=30, alpha=0.6, label='Tweaked Game', 
                       color='red', edgecolor='black')
        axes[1, 0].set_xlabel('Win/Loss Ratio')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].set_title('Win/Loss Ratio Distribution')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 4. ROI comparison
        fair_roi = (self.fair_results['net_profit'] / self.fair_results['initial_bankroll']) * 100
        tweaked_roi = (self.tweaked_results['net_profit'] / self.tweaked_results['initial_bankroll']) * 100
        
        axes[1, 1].hist(fair_roi, bins=50, alpha=0.6, label='Fair Game', 
                       color='blue', edgecolor='black')
        axes[1, 1].hist(tweaked_roi, bins=50, alpha=0.6, label='Tweaked Game', 
                       color='red', edgecolor='black')
        axes[1, 1].axvline(0, color='black', linestyle='--', linewidth=2)
        axes[1, 1].set_xlabel('ROI (%)')
        axes[1, 1].set_ylabel('Frequency')
        axes[1, 1].set_title('Return on Investment (ROI) Distribution')
        axes[1, 1].legend()
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved win/loss analysis plot to {save_path}")
        
        plt.show()
    
    def plot_bankroll_evolution(self, detailed_data: Dict[str, pd.DataFrame], 
                                num_games: int = 10, save_path: str = None):
        """
        Plot bankroll evolution over rounds for sample games.
        
        Args:
            detailed_data: Dictionary with 'fair' and 'tweaked' detailed round data
            num_games: Number of sample games to plot
            save_path: Optional path to save the figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot fair game
        for game_id in range(min(num_games, detailed_data['fair']['game_id'].max() + 1)):
            game_data = detailed_data['fair'][detailed_data['fair']['game_id'] == game_id]
            axes[0].plot(game_data['round_num'], game_data['player_bankroll'], 
                        alpha=0.5, linewidth=1)
        
        axes[0].axhline(detailed_data['fair']['player_bankroll'].iloc[0], 
                       color='black', linestyle='--', linewidth=2, label='Initial Bankroll')
        axes[0].set_xlabel('Round Number')
        axes[0].set_ylabel('Player Bankroll ($)')
        axes[0].set_title(f'Fair Game: Bankroll Evolution ({num_games} games)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot tweaked game
        for game_id in range(min(num_games, detailed_data['tweaked']['game_id'].max() + 1)):
            game_data = detailed_data['tweaked'][detailed_data['tweaked']['game_id'] == game_id]
            axes[1].plot(game_data['round_num'], game_data['player_bankroll'], 
                        alpha=0.5, linewidth=1, color='red')
        
        axes[1].axhline(detailed_data['tweaked']['player_bankroll'].iloc[0], 
                       color='black', linestyle='--', linewidth=2, label='Initial Bankroll')
        axes[1].set_xlabel('Round Number')
        axes[1].set_ylabel('Player Bankroll ($)')
        axes[1].set_title(f'Tweaked Game: Bankroll Evolution ({num_games} games)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Saved bankroll evolution plot to {save_path}")
        
        plt.show()
    
    def create_all_plots(self, detailed_data: Dict[str, pd.DataFrame] = None, 
                        output_dir: str = None):
        """
        Create all visualization plots.
        
        Args:
            detailed_data: Optional detailed round data for bankroll evolution
            output_dir: Optional directory to save all plots
        """
        print("\n" + "=" * 80)
        print("CREATING VISUALIZATIONS")
        print("=" * 80)
        
        # Profit distributions
        print("\n1. Generating profit distribution plots...")
        save_path = f"{output_dir}/profit_distributions.png" if output_dir else None
        self.plot_profit_distributions(save_path)
        
        # House profit
        print("\n2. Generating house profit plots...")
        save_path = f"{output_dir}/house_profit.png" if output_dir else None
        self.plot_house_profit(save_path)
        
        # Win/Loss analysis
        print("\n3. Generating win/loss analysis plots...")
        save_path = f"{output_dir}/win_loss_analysis.png" if output_dir else None
        self.plot_win_loss_analysis(save_path)
        
        # Bankroll evolution (if detailed data provided)
        if detailed_data:
            print("\n4. Generating bankroll evolution plots...")
            save_path = f"{output_dir}/bankroll_evolution.png" if output_dir else None
            self.plot_bankroll_evolution(detailed_data, save_path=save_path)
        
        print("\n✓ All visualizations complete!")
