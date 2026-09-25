"""
Data models and typed schemas for Speculative-Swarm.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
import time


@dataclass
class SpeculativeDraftStep:
    step_index: int
    draft_model: str # "DeepSeek V4.1-Flash" or "Gemini 3.8 Flash"
    tool_name: str
    tool_args: Dict[str, Any]
    sandboxed_output: Dict[str, Any]
    confidence: float = 0.95
    is_executed: bool = True
    draft_latency_ms: float = 120.0


@dataclass
class VerificationVerdict:
    is_fully_accepted: bool
    accepted_count: int
    rejected_at_index: Optional[int] = None
    rejected_reason: Optional[str] = None
    committed_steps: List[SpeculativeDraftStep] = field(default_factory=list)
    rollback_needed: bool = False
    verifier_model: str = "Claude Opus 5.5"


@dataclass
class SpeculativeMetrics:
    total_steps: int
    drafted_steps: int
    accepted_steps: int
    acceptance_rate_pct: float
    baseline_latency_sec: float
    speculative_latency_sec: float
    speedup_factor: float
