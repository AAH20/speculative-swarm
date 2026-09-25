"""
Speculative-Swarm: Speculative Macro-Execution Engine for Autonomous AI Agents.
Accelerates multi-turn agent runs by 10x using DeepSeek V4.1-Flash drafting and Claude Opus 5.5 batch verification.
"""

from .models import (
    SpeculativeDraftStep,
    VerificationVerdict,
    SpeculativeMetrics,
)
from .draft_engine import DraftEngine
from .verifier_arbiter import VerifierArbiter

__version__ = "1.0.0"
__all__ = [
    "SpeculativeDraftStep",
    "VerificationVerdict",
    "SpeculativeMetrics",
    "DraftEngine",
    "VerifierArbiter",
]
