"""
Color Game Model
----------------
This module implements the Filipino "Color Game" (Perya game) with both fair and tweaked versions.

Game Rules:
- Players bet on one of 6 colors: Red, Blue, Yellow, White, Green, Pink
- Three dice with these colors are rolled
- Payouts:
  * 1 die matches: 1:1 (bet $1, win $1 + original $1 = $2)
  * 2 dice match: 2:1 (bet $1, win $2 + original $1 = $3)
  * 3 dice match: 3:1 (bet $1, win $3 + original $1 = $4)
  * 0 dice match: lose bet
"""

import numpy as np
from typing import Dict, List, Tuple


class ColorGame:
    """
    Fair Color Game Model
    
    In a fair game, each color has equal probability (1/6) on each die.
    """
    
    COLORS = ['Red', 'Blue', 'Yellow', 'White', 'Green', 'Pink']
    
    def __init__(self, initial_bankroll: float = 1000.0):
        """
        Initialize the Color Game.
        
        Args:
            initial_bankroll: Starting amount of money for the player
        """
        self.initial_bankroll = initial_bankroll
        self.player_bankroll = initial_bankroll
        self.house_profit = 0.0
        self.game_history = []
        
    def roll_dice(self, num_dice: int = 3) -> List[str]:
        """
        Roll the dice with fair probabilities.
        
        Args:
            num_dice: Number of dice to roll
            
        Returns:
            List of colors from the dice roll
        """
        return list(np.random.choice(self.COLORS, size=num_dice, replace=True))
    
    def calculate_payout(self, bet_color: str, dice_results: List[str], bet_amount: float) -> Tuple[float, int]:
        """
        Calculate the payout based on how many dice match the bet color.
        
        Args:
            bet_color: The color the player bet on
            dice_results: Results from rolling the dice
            bet_amount: Amount of money bet
            
        Returns:
            Tuple of (net_winnings, matches)
            - net_winnings: positive if player wins, negative if player loses
            - matches: number of matching dice
        """
        matches = dice_results.count(bet_color)
        
        if matches == 0:
            # Player loses the bet
            return -bet_amount, 0
        elif matches == 1:
            # 1:1 payout - player gets bet back plus equal amount
            return bet_amount, 1
        elif matches == 2:
            # 2:1 payout - player gets bet back plus 2x bet
            return 2 * bet_amount, 2
        else:  # matches == 3
            # 3:1 payout - player gets bet back plus 3x bet
            return 3 * bet_amount, 3
    
    def play_round(self, bet_color: str, bet_amount: float) -> Dict:
        """
        Play one round of the Color Game.
        
        Args:
            bet_color: Color to bet on
            bet_amount: Amount to bet
            
        Returns:
            Dictionary with round results
        """
        if bet_color not in self.COLORS:
            raise ValueError(f"Invalid color. Choose from {self.COLORS}")
        
        if bet_amount > self.player_bankroll:
            raise ValueError(f"Insufficient funds. Bankroll: ${self.player_bankroll:.2f}")
        
        # Roll the dice
        dice_results = self.roll_dice()
        
        # Calculate payout
        net_winnings, matches = self.calculate_payout(bet_color, dice_results, bet_amount)
        
        # Update bankrolls
        self.player_bankroll += net_winnings
        self.house_profit -= net_winnings
        
        # Record game history
        round_result = {
            'bet_color': bet_color,
            'bet_amount': bet_amount,
            'dice_results': dice_results,
            'matches': matches,
            'net_winnings': net_winnings,
            'player_bankroll': self.player_bankroll,
            'house_profit': self.house_profit
        }
        self.game_history.append(round_result)
        
        return round_result
    
    def reset(self):
        """Reset the game to initial state."""
        self.player_bankroll = self.initial_bankroll
        self.house_profit = 0.0
        self.game_history = []
    
    def get_theoretical_house_edge(self) -> float:
        """
        Calculate the theoretical house edge for this game.
        
        Returns:
            House edge as a decimal (0.0 means fair, positive means house advantage)
        """
        # For a fair Color Game:
        # P(0 matches) = (5/6)^3 = 125/216 ≈ 0.5787
        # P(1 match) = C(3,1) * (1/6) * (5/6)^2 = 75/216 ≈ 0.3472
        # P(2 matches) = C(3,2) * (1/6)^2 * (5/6) = 15/216 ≈ 0.0694
        # P(3 matches) = (1/6)^3 = 1/216 ≈ 0.0046
        
        prob_0 = (5/6) ** 3
        prob_1 = 3 * (1/6) * (5/6) ** 2
        prob_2 = 3 * (1/6) ** 2 * (5/6)
        prob_3 = (1/6) ** 3
        
        # Expected value for player (per $1 bet)
        ev = prob_0 * (-1) + prob_1 * 1 + prob_2 * 2 + prob_3 * 3
        
        # House edge is negative of player's expected value
        return -ev


class TweakedColorGame(ColorGame):
    """
    Tweaked Color Game Model with House Edge
    
    This version introduces house advantage through:
    1. Weighted dice probabilities (house color appears more often)
    2. Modified payout structure
    """
    
    def __init__(self, initial_bankroll: float = 1000.0, 
                 house_color: str = 'Red',
                 house_color_weight: float = 0.20,
                 payout_modifier: float = 0.95):
        """
        Initialize the Tweaked Color Game.
        
        Args:
            initial_bankroll: Starting amount of money for the player
            house_color: The color that appears more frequently
            house_color_weight: Probability of house color appearing (default 0.20 vs fair 0.1667)
            payout_modifier: Multiplier for payouts (< 1.0 reduces payouts, creating house edge)
        """
        super().__init__(initial_bankroll)
        self.house_color = house_color
        self.house_color_weight = house_color_weight
        self.payout_modifier = payout_modifier
        
        # Calculate probabilities for weighted dice
        # House color gets house_color_weight, others split remaining probability
        other_weight = (1 - house_color_weight) / (len(self.COLORS) - 1)
        self.probabilities = [
            house_color_weight if color == house_color else other_weight 
            for color in self.COLORS
        ]
    
    def roll_dice(self, num_dice: int = 3) -> List[str]:
        """
        Roll the dice with weighted probabilities favoring the house color.
        
        Args:
            num_dice: Number of dice to roll
            
        Returns:
            List of colors from the dice roll
        """
        return list(np.random.choice(self.COLORS, size=num_dice, replace=True, p=self.probabilities))
    
    def calculate_payout(self, bet_color: str, dice_results: List[str], bet_amount: float) -> Tuple[float, int]:
        """
        Calculate the payout with modified payout structure.
        
        Args:
            bet_color: The color the player bet on
            dice_results: Results from rolling the dice
            bet_amount: Amount of money bet
            
        Returns:
            Tuple of (net_winnings, matches)
        """
        matches = dice_results.count(bet_color)
        
        if matches == 0:
            return -bet_amount, 0
        elif matches == 1:
            # Modified 1:1 payout becomes 0.95:1
            return bet_amount * self.payout_modifier, 1
        elif matches == 2:
            # Modified 2:1 payout becomes 1.9:1
            return 2 * bet_amount * self.payout_modifier, 2
        else:  # matches == 3
            # Modified 3:1 payout becomes 2.85:1
            return 3 * bet_amount * self.payout_modifier, 3
    
    def get_theoretical_house_edge(self) -> float:
        """
        Calculate the theoretical house edge for the tweaked game.
        
        This is more complex due to weighted probabilities.
        """
        # For house color bet
        p_house = self.house_color_weight
        p_other = (1 - self.house_color_weight) / (len(self.COLORS) - 1)
        
        prob_0 = (1 - p_house) ** 3
        prob_1 = 3 * p_house * (1 - p_house) ** 2
        prob_2 = 3 * p_house ** 2 * (1 - p_house)
        prob_3 = p_house ** 3
        
        # Expected value with modified payouts
        ev = (prob_0 * (-1) + 
              prob_1 * self.payout_modifier + 
              prob_2 * 2 * self.payout_modifier + 
              prob_3 * 3 * self.payout_modifier)
        
        return -ev
