"""
Analysis Module
---------------
Exploratory Data Analysis (EDA) and statistical comparison of game simulations.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from scipy import stats


class GameAnalyzer:
    """
    Performs statistical analysis on game simulation results.
    """
    
    def __init__(self, fair_results: pd.DataFrame, tweaked_results: pd.DataFrame):
        """
        Initialize analyzer with simulation results.
        
        Args:
            fair_results: DataFrame from fair game simulations
            tweaked_results: DataFrame from tweaked game simulations
        """
        self.fair_results = fair_results
        self.tweaked_results = tweaked_results
    
    def calculate_summary_statistics(self) -> Dict[str, Dict]:
        """
        Calculate summary statistics for both game types.
        
        Returns:
            Dictionary with statistics for fair and tweaked games
        """
        def get_stats(df: pd.DataFrame) -> Dict:
            return {
                'mean_profit': df['net_profit'].mean(),
                'median_profit': df['net_profit'].median(),
                'std_profit': df['net_profit'].std(),
                'min_profit': df['net_profit'].min(),
                'max_profit': df['net_profit'].max(),
                'win_rate': (df['net_profit'] > 0).mean(),
                'avg_house_profit': df['house_profit'].mean(),
                'total_house_profit': df['house_profit'].sum(),
                'avg_rounds_played': df['rounds_played'].mean(),
                'bankruptcy_rate': (df['final_bankroll'] == 0).mean(),
                'avg_total_wagered': df['total_wagered'].mean(),
            }
        
        return {
            'fair': get_stats(self.fair_results),
            'tweaked': get_stats(self.tweaked_results)
        }
    
    def calculate_house_edge(self) -> Dict[str, float]:
        """
        Calculate empirical house edge from simulation results.
        
        House edge = Average house profit / Total amount wagered
        
        Returns:
            Dictionary with house edge for both games
        """
        fair_edge = (self.fair_results['house_profit'].sum() / 
                     self.fair_results['total_wagered'].sum())
        
        tweaked_edge = (self.tweaked_results['house_profit'].sum() / 
                       self.tweaked_results['total_wagered'].sum())
        
        return {
            'fair': fair_edge,
            'tweaked': tweaked_edge,
            'difference': tweaked_edge - fair_edge
        }
    
    def perform_hypothesis_test(self) -> Dict:
        """
        Perform statistical hypothesis test to compare mean profits.
        
        H0: Mean profit in fair game = Mean profit in tweaked game
        H1: Mean profit in fair game ≠ Mean profit in tweaked game
        
        Returns:
            Dictionary with test results
        """
        # Two-sample t-test
        t_stat, p_value = stats.ttest_ind(
            self.fair_results['net_profit'],
            self.tweaked_results['net_profit']
        )
        
        # Mann-Whitney U test (non-parametric alternative)
        u_stat, u_pvalue = stats.mannwhitneyu(
            self.fair_results['net_profit'],
            self.tweaked_results['net_profit'],
            alternative='two-sided'
        )
        
        return {
            't_test': {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            },
            'mann_whitney': {
                'u_statistic': u_stat,
                'p_value': u_pvalue,
                'significant': u_pvalue < 0.05
            }
        }
    
    def calculate_roi(self) -> Dict[str, Dict]:
        """
        Calculate Return on Investment (ROI) statistics.
        
        Returns:
            Dictionary with ROI statistics
        """
        def get_roi_stats(df: pd.DataFrame) -> Dict:
            roi = (df['net_profit'] / df['initial_bankroll']) * 100
            return {
                'mean_roi': roi.mean(),
                'median_roi': roi.median(),
                'std_roi': roi.std(),
                'min_roi': roi.min(),
                'max_roi': roi.max()
            }
        
        return {
            'fair': get_roi_stats(self.fair_results),
            'tweaked': get_roi_stats(self.tweaked_results)
        }
    
    def analyze_profit_distribution(self) -> Dict[str, Dict]:
        """
        Analyze the distribution of profits.
        
        Returns:
            Dictionary with distribution characteristics
        """
        def get_distribution_stats(df: pd.DataFrame) -> Dict:
            profits = df['net_profit']
            return {
                'skewness': stats.skew(profits),
                'kurtosis': stats.kurtosis(profits),
                'percentile_25': profits.quantile(0.25),
                'percentile_50': profits.quantile(0.50),
                'percentile_75': profits.quantile(0.75),
                'percentile_95': profits.quantile(0.95),
                'percentile_5': profits.quantile(0.05),
            }
        
        return {
            'fair': get_distribution_stats(self.fair_results),
            'tweaked': get_distribution_stats(self.tweaked_results)
        }
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive text report of the analysis.
        
        Returns:
            Formatted report string
        """
        summary = self.calculate_summary_statistics()
        house_edge = self.calculate_house_edge()
        hypothesis = self.perform_hypothesis_test()
        roi = self.calculate_roi()
        distribution = self.analyze_profit_distribution()
        
        report = []
        report.append("=" * 80)
        report.append("COLOR GAME SIMULATION: ANALYSIS REPORT")
        report.append("=" * 80)
        
        # Summary Statistics
        report.append("\n1. SUMMARY STATISTICS")
        report.append("-" * 80)
        report.append(f"{'Metric':<30} {'Fair Game':<25} {'Tweaked Game':<25}")
        report.append("-" * 80)
        
        metrics = [
            ('Mean Profit', 'mean_profit', '${:.2f}'),
            ('Median Profit', 'median_profit', '${:.2f}'),
            ('Std Dev Profit', 'std_profit', '${:.2f}'),
            ('Min Profit', 'min_profit', '${:.2f}'),
            ('Max Profit', 'max_profit', '${:.2f}'),
            ('Win Rate', 'win_rate', '{:.2%}'),
            ('Avg House Profit', 'avg_house_profit', '${:.2f}'),
            ('Total House Profit', 'total_house_profit', '${:.2f}'),
            ('Avg Rounds Played', 'avg_rounds_played', '{:.2f}'),
            ('Bankruptcy Rate', 'bankruptcy_rate', '{:.2%}'),
        ]
        
        for label, key, fmt in metrics:
            fair_val = fmt.format(summary['fair'][key])
            tweaked_val = fmt.format(summary['tweaked'][key])
            report.append(f"{label:<30} {fair_val:<25} {tweaked_val:<25}")
        
        # House Edge Analysis
        report.append("\n2. HOUSE EDGE ANALYSIS")
        report.append("-" * 80)
        report.append(f"Fair Game House Edge:       {house_edge['fair']:.4%}")
        report.append(f"Tweaked Game House Edge:    {house_edge['tweaked']:.4%}")
        report.append(f"Difference:                 {house_edge['difference']:.4%}")
        report.append(f"\nInterpretation: The tweaked game has a house edge that is ")
        report.append(f"{abs(house_edge['difference']):.4%} {'higher' if house_edge['difference'] > 0 else 'lower'} than the fair game.")
        
        # ROI Analysis
        report.append("\n3. RETURN ON INVESTMENT (ROI)")
        report.append("-" * 80)
        report.append(f"{'Metric':<30} {'Fair Game':<25} {'Tweaked Game':<25}")
        report.append("-" * 80)
        report.append(f"{'Mean ROI':<30} {roi['fair']['mean_roi']:<24.2f}% {roi['tweaked']['mean_roi']:<24.2f}%")
        report.append(f"{'Median ROI':<30} {roi['fair']['median_roi']:<24.2f}% {roi['tweaked']['median_roi']:<24.2f}%")
        report.append(f"{'Std Dev ROI':<30} {roi['fair']['std_roi']:<24.2f}% {roi['tweaked']['std_roi']:<24.2f}%")
        
        # Distribution Analysis
        report.append("\n4. PROFIT DISTRIBUTION ANALYSIS")
        report.append("-" * 80)
        report.append(f"{'Metric':<30} {'Fair Game':<25} {'Tweaked Game':<25}")
        report.append("-" * 80)
        report.append(f"{'Skewness':<30} {distribution['fair']['skewness']:<24.4f} {distribution['tweaked']['skewness']:<24.4f}")
        report.append(f"{'Kurtosis':<30} {distribution['fair']['kurtosis']:<24.4f} {distribution['tweaked']['kurtosis']:<24.4f}")
        report.append(f"{'5th Percentile':<30} ${distribution['fair']['percentile_5']:<23.2f} ${distribution['tweaked']['percentile_5']:<23.2f}")
        report.append(f"{'95th Percentile':<30} ${distribution['fair']['percentile_95']:<23.2f} ${distribution['tweaked']['percentile_95']:<23.2f}")
        
        # Hypothesis Testing
        report.append("\n5. STATISTICAL HYPOTHESIS TESTING")
        report.append("-" * 80)
        report.append("H0: Mean profit in fair game = Mean profit in tweaked game")
        report.append("H1: Mean profit in fair game ≠ Mean profit in tweaked game")
        report.append(f"\nTwo-Sample t-test:")
        report.append(f"  t-statistic: {hypothesis['t_test']['t_statistic']:.4f}")
        report.append(f"  p-value: {hypothesis['t_test']['p_value']:.6f}")
        report.append(f"  Significant at α=0.05: {'YES' if hypothesis['t_test']['significant'] else 'NO'}")
        report.append(f"\nMann-Whitney U test (non-parametric):")
        report.append(f"  U-statistic: {hypothesis['mann_whitney']['u_statistic']:.4f}")
        report.append(f"  p-value: {hypothesis['mann_whitney']['p_value']:.6f}")
        report.append(f"  Significant at α=0.05: {'YES' if hypothesis['mann_whitney']['significant'] else 'NO'}")
        
        # Conclusions
        report.append("\n6. KEY FINDINGS")
        report.append("-" * 80)
        
        profit_diff = summary['fair']['mean_profit'] - summary['tweaked']['mean_profit']
        report.append(f"• The fair game yields an average profit of ${summary['fair']['mean_profit']:.2f} per session")
        report.append(f"• The tweaked game yields an average profit of ${summary['tweaked']['mean_profit']:.2f} per session")
        report.append(f"• Players lose ${abs(profit_diff):.2f} more on average in the tweaked game")
        report.append(f"• The house edge increased by {house_edge['difference']:.4%} in the tweaked version")
        report.append(f"• Win rate decreased from {summary['fair']['win_rate']:.2%} to {summary['tweaked']['win_rate']:.2%}")
        
        if hypothesis['t_test']['significant']:
            report.append(f"• Statistical tests confirm the difference is significant (p < 0.05)")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
