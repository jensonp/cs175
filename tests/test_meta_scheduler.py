from __future__ import annotations

import pytest

from scheduler.meta import make_meta_scheduler
from scheduler.models import Job
from scheduler.policies import EDFPolicy, SPTPolicy


def test_meta_scheduler_updates_weights_after_observation() -> None:
    jobs = [
        Job(
            job_id="job-a",
            release_time=0,
            processing_time=5,
            predicted_processing_time=5.0,
            confidence=0.9,
            deadline=3,
        ),
        Job(
            job_id="job-b",
            release_time=0,
            processing_time=1,
            predicted_processing_time=1.0,
            confidence=0.8,
            deadline=6,
        ),
    ]
    meta = make_meta_scheduler([EDFPolicy(), SPTPolicy()])

    _, _, before = meta.choose_job(jobs, now=0)
    meta.observe_outcome(now=0)
    after = meta.snapshot()

    assert sum(after.values()) == pytest.approx(1.0)
    assert after != before


def test_meta_scheduler_returns_expert_name() -> None:
    jobs = [
        Job(
            job_id="job-a",
            release_time=0,
            processing_time=2,
            predicted_processing_time=2.0,
            confidence=0.9,
            deadline=5,
        )
    ]
    meta = make_meta_scheduler([EDFPolicy(), SPTPolicy()])
    _, selected_expert, _ = meta.choose_job(jobs, now=0)
    assert selected_expert in {"edf", "spt"}
