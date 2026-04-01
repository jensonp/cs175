from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import List

from scheduler.models import Job


def _deadline_key(job: Job) -> tuple[int, float, str]:
    return (job.deadline, job.predicted_processing_time, job.job_id)


def _predicted_length_key(job: Job) -> tuple[float, int, str]:
    return (job.predicted_processing_time, job.deadline, job.job_id)


class ExpertPolicy(ABC):
    name: str

    @abstractmethod
    def rank_jobs(self, jobs: Sequence[Job], now: int) -> List[Job]:
        raise NotImplementedError

    def choose_job(self, jobs: Sequence[Job], now: int) -> Job:
        ranked = self.rank_jobs(jobs, now)
        if not ranked:
            raise ValueError("cannot choose from an empty job list")
        return ranked[0]


@dataclass
class EDFPolicy(ExpertPolicy):
    name: str = "edf"

    def rank_jobs(self, jobs: Sequence[Job], now: int) -> List[Job]:
        del now
        return sorted(jobs, key=_deadline_key)


@dataclass
class SPTPolicy(ExpertPolicy):
    name: str = "spt"

    def rank_jobs(self, jobs: Sequence[Job], now: int) -> List[Job]:
        del now
        return sorted(jobs, key=_predicted_length_key)


@dataclass
class LeastSlackPolicy(ExpertPolicy):
    name: str = "least-slack"

    def rank_jobs(self, jobs: Sequence[Job], now: int) -> List[Job]:
        return sorted(
            jobs,
            key=lambda job: (
                job.deadline - now - int(job.predicted_processing_time),
                job.deadline,
                job.job_id,
            ),
        )


@dataclass
class ConfidenceGatedEDFSPTPolicy(ExpertPolicy):
    threshold: float = 0.65
    name: str = "confidence-gated-edf-spt"

    def rank_jobs(self, jobs: Sequence[Job], now: int) -> List[Job]:
        del now
        high_conf = [job for job in jobs if job.confidence >= self.threshold]
        low_conf = [job for job in jobs if job.confidence < self.threshold]
        return sorted(high_conf, key=_predicted_length_key) + sorted(low_conf, key=_deadline_key)


def default_experts() -> List[ExpertPolicy]:
    return [
        EDFPolicy(),
        SPTPolicy(),
        LeastSlackPolicy(),
        ConfidenceGatedEDFSPTPolicy(),
    ]


def policy_names(policies: Iterable[ExpertPolicy]) -> List[str]:
    return [policy.name for policy in policies]
