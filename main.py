"""
Main Application
----------------
Run Color Game simulations and generate complete analysis report.
"""

import os
import numpy as np
from color_game import ColorGame, TweakedColorGame
from simulation import GameSimulator, compare_models
from analysis import GameAnalyzer
from visualization import GameVisualizer


def main():
    """
    Main function to run the complete simulation and analysis.
    """
    print("\n" + "=" * 80)
    print("STOCHASTIC GAME SIMULATION: FILIPINO COLOR GAME")
    print("=" * 80)
    print("\nThis project explores Monte Carlo simulation of a Filipino 'Perya' game")
    print("to analyze the impact of introducing a house edge.")
    print("\n" + "=" * 80)
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # ========== CONFIGURATION ==========
    INITIAL_BANKROLL = 1000.0
    NUM_SIMULATIONS = 10000
    ROUNDS_PER_GAME = 100
    BET_AMOUNT = 10.0
    BETTING_STRATEGY = 'random'  # Options: 'random', 'single_color', 'house_color'
    
    # Tweak parameters
    HOUSE_COLOR = 'Red'
    HOUSE_COLOR_WEIGHT = 0.20  # 20% vs fair 16.67%
    PAYOUT_MODIFIER = 0.95  # 95% of fair payout
    
    print("\nSIMULATION CONFIGURATION:")
    print("-" * 80)
    print(f"  Initial Bankroll:     ${INITIAL_BANKROLL:,.2f}")
    print(f"  Number of Simulations: {NUM_SIMULATIONS:,}")
    print(f"  Rounds per Game:       {ROUNDS_PER_GAME}")
    print(f"  Bet Amount:            ${BET_AMOUNT}")
    print(f"  Betting Strategy:      {BETTING_STRATEGY}")
    print(f"\nTWEAK PARAMETERS:")
    print(f"  House Color:           {HOUSE_COLOR}")
    print(f"  House Color Weight:    {HOUSE_COLOR_WEIGHT:.2%} (vs {1/6:.2%} fair)")
    print(f"  Payout Modifier:       {PAYOUT_MODIFIER:.2%} (of fair payout)")
    
    # ========== CREATE GAME MODELS ==========
    print("\n" + "=" * 80)
    print("STEP 1: CREATING GAME MODELS")
    print("=" * 80)
    
    fair_game = ColorGame(initial_bankroll=INITIAL_BANKROLL)
    tweaked_game = TweakedColorGame(
        initial_bankroll=INITIAL_BANKROLL,
        house_color=HOUSE_COLOR,
        house_color_weight=HOUSE_COLOR_WEIGHT,
        payout_modifier=PAYOUT_MODIFIER
    )
    
    # Display theoretical house edges
    fair_edge = fair_game.get_theoretical_house_edge()
    tweaked_edge = tweaked_game.get_theoretical_house_edge()
    
    print(f"\n✓ Fair Game Model created")
    print(f"  Theoretical House Edge: {fair_edge:.4%}")
    print(f"\n✓ Tweaked Game Model created")
    print(f"  Theoretical House Edge: {tweaked_edge:.4%}")
    print(f"  Expected increase: {tweaked_edge - fair_edge:.4%}")
    
    # ========== RUN SIMULATIONS ==========
    print("\n" + "=" * 80)
    print("STEP 2: RUNNING MONTE CARLO SIMULATIONS")
    print("=" * 80)
    
    simulation_results = compare_models(
        fair_game=fair_game,
        tweaked_game=tweaked_game,
        num_simulations=NUM_SIMULATIONS,
        rounds_per_game=ROUNDS_PER_GAME,
        bet_amount=BET_AMOUNT,
        strategy=BETTING_STRATEGY
    )
    
    fair_results = simulation_results['fair']
    tweaked_results = simulation_results['tweaked']
    
    # ========== PERFORM ANALYSIS ==========
    print("\n" + "=" * 80)
    print("STEP 3: PERFORMING EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 80)
    
    analyzer = GameAnalyzer(fair_results, tweaked_results)
    
    # Generate and display report
    report = analyzer.generate_report()
    print("\n" + report)
    
    # Save report to file
    os.makedirs('results', exist_ok=True)
    with open('results/analysis_report.txt', 'w') as f:
        f.write(report)
    print(f"\n✓ Analysis report saved to: results/analysis_report.txt")
    
    # Save simulation data
    fair_results.to_csv('results/fair_game_results.csv', index=False)
    tweaked_results.to_csv('results/tweaked_game_results.csv', index=False)
    print(f"✓ Simulation data saved to: results/fair_game_results.csv and results/tweaked_game_results.csv")
    
    # ========== CREATE VISUALIZATIONS ==========
    print("\n" + "=" * 80)
    print("STEP 4: CREATING VISUALIZATIONS")
    print("=" * 80)
    
    # Get detailed round data for bankroll evolution plots
    print("\nCollecting detailed round data for visualizations...")
    fair_simulator = GameSimulator(fair_game)
    tweaked_simulator = GameSimulator(tweaked_game)
    
    fair_detailed = fair_simulator.get_detailed_round_data(
        num_games=50, 
        rounds_per_game=ROUNDS_PER_GAME,
        bet_amount=BET_AMOUNT,
        strategy=BETTING_STRATEGY
    )
    
    tweaked_detailed = tweaked_simulator.get_detailed_round_data(
        num_games=50,
        rounds_per_game=ROUNDS_PER_GAME,
        bet_amount=BET_AMOUNT,
        strategy=BETTING_STRATEGY
    )
    
    detailed_data = {
        'fair': fair_detailed,
        'tweaked': tweaked_detailed
    }
    
    # Create visualizations
    visualizer = GameVisualizer(fair_results, tweaked_results)
    visualizer.create_all_plots(detailed_data=detailed_data, output_dir='results')
    
    # ========== SUMMARY ==========
    print("\n" + "=" * 80)
    print("SIMULATION COMPLETE!")
    print("=" * 80)
    print("\nGenerated Files:")
    print("  📊 results/analysis_report.txt")
    print("  📈 results/profit_distributions.png")
    print("  📈 results/house_profit.png")
    print("  📈 results/win_loss_analysis.png")
    print("  📈 results/bankroll_evolution.png")
    print("  📄 results/fair_game_results.csv")
    print("  📄 results/tweaked_game_results.csv")
    print("\nKey Findings:")
    summary = analyzer.calculate_summary_statistics()
    house_edge = analyzer.calculate_house_edge()
    print(f"  • Fair game mean profit: ${summary['fair']['mean_profit']:.2f}")
    print(f"  • Tweaked game mean profit: ${summary['tweaked']['mean_profit']:.2f}")
    print(f"  • Empirical house edge difference: {house_edge['difference']:.4%}")
    print(f"  • Fair game win rate: {summary['fair']['win_rate']:.2%}")
    print(f"  • Tweaked game win rate: {summary['tweaked']['win_rate']:.2%}")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
