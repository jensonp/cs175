from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Dict, Tuple

from scheduler.models import Job
from scheduler.policies import ExpertPolicy


@dataclass
class MetaScheduler:
    experts: Sequence[ExpertPolicy]
    learning_rate: float = 0.8
    confidence_bonus: float = 0.35
    weights: Dict[str, float] = field(init=False)
    last_candidates: Dict[str, Job] = field(init=False, default_factory=dict)
    last_selected_expert: str = field(init=False, default="")

    def __post_init__(self) -> None:
        if not self.experts:
            raise ValueError("MetaScheduler needs at least one expert")
        self.weights = {expert.name: 1.0 for expert in self.experts}

    @property
    def name(self) -> str:
        return "meta-scheduler"

    def choose_job(self, jobs: Sequence[Job], now: int) -> Tuple[Job, str, Dict[str, float]]:
        if not jobs:
            raise ValueError("cannot choose from an empty job list")

        scores: Dict[str, float] = {}
        candidates: Dict[str, Job] = {}
        for expert in self.experts:
            candidate = expert.choose_job(jobs, now)
            candidates[expert.name] = candidate
            bonus = self.confidence_bonus * candidate.confidence
            scores[expert.name] = math.log(self.weights[expert.name]) + bonus

        selected_expert = max(scores, key=scores.get)
        self.last_candidates = candidates
        self.last_selected_expert = selected_expert
        return candidates[selected_expert], selected_expert, dict(self.weights)

    def observe_outcome(self, now: int) -> None:
        if not self.last_candidates:
            return

        updated: Dict[str, float] = {}
        for name, candidate in self.last_candidates.items():
            finish = now + candidate.processing_time
            missed = finish > candidate.deadline
            lateness = max(0, finish - candidate.deadline)
            loss = candidate.penalty * float(missed) + 0.1 * float(lateness)
            updated[name] = self.weights[name] * math.exp(-self.learning_rate * loss)

        total = sum(updated.values())
        if total <= 0:
            total = float(len(updated))
            updated = {name: 1.0 for name in updated}

        self.weights = {name: value / total for name, value in updated.items()}
        self.last_candidates = {}

    def snapshot(self) -> Dict[str, float]:
        return dict(self.weights)


def make_meta_scheduler(experts: Iterable[ExpertPolicy]) -> MetaScheduler:
    return MetaScheduler(list(experts))
