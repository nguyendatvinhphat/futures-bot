import sys, os
sys.path.insert(0, 'C:\\Users\\COHOTECH.VN\\OneDrive\\Desktop\\futures_bot')
os.chdir('C:\\Users\\COHOTECH.VN\\OneDrive\\Desktop\\futures_bot')
os.environ["PYTHONIOENCODING"] = "utf-8"

from signals.learning import signal_learner

# Test learning system
print("Testing Learning System...")

# Get overall stats
stats = signal_learner.get_overall_stats()
print(f"\nOverall Stats:")
print(f"  Total Signals: {stats['total_signals']}")
print(f"  Active: {stats['active_signals']}")
print(f"  Closed: {stats['closed_signals']}")
print(f"  Win Rate: {stats['win_rate']}%")

# Get indicator performance
perf = signal_learner.get_indicator_performance()
print(f"\nIndicator Performance:")
for ind, values in perf.items():
    for val, data in values.items():
        print(f"  {ind}={val}: {data['win_rate']}% ({data['total']} samples)")

# Get regime performance
regime = signal_learner.get_regime_performance()
print(f"\nRegime Performance:")
for r, data in regime.items():
    print(f"  {r}: {data['win_rate']}% ({data['total']} samples)")

# Get weight adjustments
adj = signal_learner.calculate_weight_adjustments()
print(f"\nWeight Adjustments:")
for ind, a in adj.items():
    print(f"  {ind}: {a['original']} -> {a['adjusted']} ({a['reason']})")

# Generate report
report = signal_learner.format_learning_report()
print(f"\nReport length: {len(report)} chars")
print("\nReport preview:")
print(report[:500])
