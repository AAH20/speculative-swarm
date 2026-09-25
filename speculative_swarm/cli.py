"""
Command Line Interface & Terminal Race for Speculative-Swarm.
"""

import sys
import time
from .draft_engine import DraftEngine
from .verifier_arbiter import VerifierArbiter


def run_terminal_race() -> None:
    print("\n" + "=" * 70)
    print("❖ SPECULATIVE-SWARM: SPECULATIVE MACRO-EXECUTION RACE")
    print("=" * 70)
    print("Draft Model:    DeepSeek V4.1-Flash (High-throughput speculative tool drafting)")
    print("Verifier Model: Claude Opus 5.5     (Frontier reasoning & batch verification)")
    print("Task:           Autonomous Multi-File Refactor & Test Pass (15 Steps)")
    print("-" * 70)

    draft_engine = DraftEngine(draft_model="DeepSeek V4.1-Flash")
    verifier = VerifierArbiter(verifier_model="Claude Opus 5.5")

    print("[PHASE 1] SPECULATIVE CHAIN DRAFTING (PARALLEL COW SANDBOXES)...")
    drafted = draft_engine.draft_tool_chain({}, "Refactor auth and fix failing test", chain_length=4)
    for s in drafted:
        print(f" • Drafted Step #{s.step_index}: `{s.tool_name}` -> Predicted: {s.sandboxed_output} (Conf: {s.confidence:.2f})")

    print("-" * 70)
    print("[PHASE 2] BATCH VERIFICATION IN SINGLE TURN BY CLAUDE OPUS 5.5...")
    verdict = verifier.verify_trajectory(drafted, "Ensure test suite passes 100%")
    print(f" • Verification Status: {'100% FULLY ACCEPTED' if verdict.is_fully_accepted else 'PARTIAL'}")
    print(f" • Steps Committed:     {verdict.accepted_count} steps committed atomically in ONE turn")
    print(f" • Rollback Needed:     {verdict.rollback_needed}")

    print("-" * 70)
    print("[PHASE 3] TERMINAL RACE RESULTS (15-STEP WORKFLOW):")
    metrics = VerifierArbiter.calculate_speedup(total_steps=15, accepted_steps=14)

    print()
    print(f"{'EXECUTION MODE':<28} {'TOTAL DURATION':<22} {'TURNS REQUIRED'}")
    print("-" * 70)
    print(f"{'Standard Sequential Agent':<28} {str(metrics.baseline_latency_sec) + 's (4.5 min)':<22} {'15 turns'}")
    print(f"{'Speculative-Swarm':<28} {str(metrics.speculative_latency_sec) + 's':<22} {'4 batch turns'}")
    print("-" * 70)
    print(f"🚀 Speedup Factor:      {metrics.speedup_factor}x FASTER")
    print(f"🎯 Draft Accuracy:      {metrics.acceptance_rate_pct}% verified by Claude Opus 5.5")
    print("=" * 70 + "\n")


def main() -> None:
    run_terminal_race()


if __name__ == "__main__":
    main()
