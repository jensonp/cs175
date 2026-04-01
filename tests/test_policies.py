from __future__ import annotations

from scheduler.models import Job
from scheduler.policies import ConfidenceGatedEDFSPTPolicy, EDFPolicy, LeastSlackPolicy, SPTPolicy


def _jobs() -> list[Job]:
    return [
        Job(
            job_id="job-a",
            release_time=0,
            processing_time=5,
            predicted_processing_time=2.0,
            confidence=0.9,
            deadline=10,
        ),
        Job(
            job_id="job-b",
            release_time=0,
            processing_time=2,
            predicted_processing_time=3.0,
            confidence=0.4,
            deadline=7,
        ),
        Job(
            job_id="job-c",
            release_time=0,
            processing_time=3,
            predicted_processing_time=1.0,
            confidence=0.8,
            deadline=12,
        ),
    ]


def test_edf_picks_earliest_deadline() -> None:
    selected = EDFPolicy().choose_job(_jobs(), now=0)
    assert selected.job_id == "job-b"


def test_spt_picks_shortest_predicted_job() -> None:
    selected = SPTPolicy().choose_job(_jobs(), now=0)
    assert selected.job_id == "job-c"


def test_least_slack_uses_deadline_pressure() -> None:
    selected = LeastSlackPolicy().choose_job(_jobs(), now=4)
    assert selected.job_id == "job-b"


def test_confidence_gated_policy_prioritizes_high_confidence_short_jobs() -> None:
    selected = ConfidenceGatedEDFSPTPolicy(threshold=0.7).choose_job(_jobs(), now=0)
    assert selected.job_id == "job-c"
