from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Job:
    job_id: str
    release_time: int
    processing_time: int
    predicted_processing_time: float
    confidence: float
    deadline: int
    penalty: float = 1.0

    def __post_init__(self) -> None:
        if self.processing_time <= 0:
            raise ValueError("processing_time must be positive")
        if self.predicted_processing_time <= 0:
            raise ValueError("predicted_processing_time must be positive")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        if self.deadline < self.release_time:
            raise ValueError("deadline must be >= release_time")


@dataclass
class MachineState:
    machine_id: int
    available_at: int = 0


@dataclass(frozen=True)
class ScheduledJob:
    job_id: str
    machine_id: int
    start_time: int
    finish_time: int
    deadline: int
    lateness: int
    missed_deadline: bool
    penalty_paid: float
    selected_by: str


@dataclass(frozen=True)
class DecisionRecord:
    time: int
    machine_id: int
    selected_job_id: str
    selected_policy: str
    selected_expert: str
    available_job_ids: List[str]
    weight_snapshot: Dict[str, float]


@dataclass(frozen=True)
class MetricsSummary:
    policy_name: str
    total_jobs: int
    missed_deadlines: int
    total_penalty: float
    average_lateness: float
    makespan: int
    machine_utilization: float


@dataclass
class RunTrace:
    policy_name: str
    num_machines: int
    scheduled_jobs: List[ScheduledJob] = field(default_factory=list)
    decisions: List[DecisionRecord] = field(default_factory=list)
