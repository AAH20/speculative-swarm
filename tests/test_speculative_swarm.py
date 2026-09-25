"""
Unit tests for Speculative-Swarm using standard unittest.
"""

import unittest
from speculative_swarm.models import SpeculativeDraftStep
from speculative_swarm.draft_engine import DraftEngine
from speculative_swarm.verifier_arbiter import VerifierArbiter


class TestSpeculativeSwarm(unittest.TestCase):
    def setUp(self):
        self.draft_engine = DraftEngine(draft_model="DeepSeek V4.1-Flash")
        self.verifier = VerifierArbiter(verifier_model="Claude Opus 5.5")

    def test_draft_chain_generation(self):
        steps = self.draft_engine.draft_tool_chain({}, "Fix test bug", chain_length=3)
        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[0].tool_name, "git_diff")
        self.assertEqual(steps[1].tool_name, "run_pytest")
        self.assertTrue(steps[0].is_executed)

    def test_full_acceptance_trajectory(self):
        steps = self.draft_engine.draft_tool_chain({}, "Fix bug", chain_length=3)
        verdict = self.verifier.verify_trajectory(steps, "goal")

        self.assertTrue(verdict.is_fully_accepted)
        self.assertEqual(verdict.accepted_count, 3)
        self.assertFalse(verdict.rollback_needed)
        self.assertEqual(len(verdict.committed_steps), 3)

    def test_partial_rejection_and_rollback(self):
        steps = self.draft_engine.draft_tool_chain({}, "Fix bug", chain_length=3)
        # Taint step 2 with invalid arguments
        steps[1].tool_args = {"invalid_flag": "--force-drop-tables"}

        verdict = self.verifier.verify_trajectory(steps, "goal")
        self.assertFalse(verdict.is_fully_accepted)
        self.assertEqual(verdict.accepted_count, 1) # Only step 1 accepted
        self.assertEqual(verdict.rejected_at_index, 2)
        self.assertTrue(verdict.rollback_needed)

    def test_speedup_calculation(self):
        metrics = VerifierArbiter.calculate_speedup(total_steps=12, accepted_steps=12)
        self.assertGreater(metrics.speedup_factor, 5.0)
        self.assertEqual(metrics.acceptance_rate_pct, 100.0)


if __name__ == "__main__":
    unittest.main()
