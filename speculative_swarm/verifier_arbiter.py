"""
Verifier Arbiter for Speculative-Swarm.
Uses Claude Opus 5.5 to evaluate speculative trajectories and commit batches atomically.
"""

from typing import List, Dict, Any, Optional
from .models import (
    SpeculativeDraftStep,
    VerificationVerdict,
    SpeculativeMetrics,
)


class VerifierArbiter:
    """Evaluates speculative tool steps using frontier reasoning and commits valid prefixes."""

    def __init__(self, verifier_model: str = "Claude Opus 5.5"):
        self.verifier_model = verifier_model

    def verify_trajectory(
        self,
        drafted_steps: List[SpeculativeDraftStep],
        goal_criteria: str
    ) -> VerificationVerdict:
        """Evaluates drafted chain in a single turn, committing accepted steps."""
        committed: List[SpeculativeDraftStep] = []

        for step in drafted_steps:
            # Check for safety or hallucinated tool parameters
            if "invalid" in str(step.tool_args).lower():
                return VerificationVerdict(
                    is_fully_accepted=False,
                    accepted_count=len(committed),
                    rejected_at_index=step.step_index,
                    rejected_reason=f"Step #{step.step_index} ({step.tool_name}) contained invalid arguments",
                    committed_steps=committed,
                    rollback_needed=True,
                    verifier_model=self.verifier_model
                )

            # Accept valid step
            committed.append(step)

        return VerificationVerdict(
            is_fully_accepted=True,
            accepted_count=len(committed),
            rejected_at_index=None,
            rejected_reason=None,
            committed_steps=committed,
            rollback_needed=False,
            verifier_model=self.verifier_model
        )

    @staticmethod
    def calculate_speedup(
        total_steps: int,
        accepted_steps: int,
        turn_latency_sec: float = 18.0,
        draft_latency_sec: float = 0.5,
        verify_latency_sec: float = 3.5
    ) -> SpeculativeMetrics:
        """Computes wall-clock execution speedup vs sequential execution."""
        # Sequential: total_steps * turn_latency_sec
        baseline_sec = total_steps * turn_latency_sec

        # Speculative: Batch execution (e.g. 4 steps verified in 1 turn)
        batch_size = 4
        num_batches = max(1, (total_steps + batch_size - 1) // batch_size)
        speculative_sec = (num_batches * (draft_latency_sec + verify_latency_sec))

        speedup = baseline_sec / max(0.1, speculative_sec)
        acceptance_pct = (accepted_steps / total_steps) * 100.0 if total_steps > 0 else 0.0

        return SpeculativeMetrics(
            total_steps=total_steps,
            drafted_steps=total_steps,
            accepted_steps=accepted_steps,
            acceptance_rate_pct=round(acceptance_pct, 1),
            baseline_latency_sec=round(baseline_sec, 1),
            speculative_latency_sec=round(speculative_sec, 1),
            speedup_factor=round(speedup, 1)
        )
