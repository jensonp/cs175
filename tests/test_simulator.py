from __future__ import annotations

from scheduler.models import Job
from scheduler.policies import EDFPolicy
from scheduler.simulator import run_policy


def test_run_policy_schedules_each_job_once() -> None:
    jobs = [
        Job(
            job_id="job-a",
            release_time=0,
            processing_time=3,
            predicted_processing_time=2.8,
            confidence=0.7,
            deadline=7,
        ),
        Job(
            job_id="job-b",
            release_time=0,
            processing_time=1,
            predicted_processing_time=1.2,
            confidence=0.8,
            deadline=4,
        ),
        Job(
            job_id="job-c",
            release_time=1,
            processing_time=2,
            predicted_processing_time=2.1,
            confidence=0.6,
            deadline=8,
        ),
    ]

    trace = run_policy(EDFPolicy(), jobs, num_machines=2)
    assert len(trace.scheduled_jobs) == len(jobs)
    assert {job.job_id for job in trace.scheduled_jobs} == {"job-a", "job-b", "job-c"}


def test_machine_assignments_do_not_overlap() -> None:
    jobs = [
        Job(
            job_id="job-a",
            release_time=0,
            processing_time=2,
            predicted_processing_time=2.0,
            confidence=0.9,
            deadline=5,
        ),
        Job(
            job_id="job-b",
            release_time=0,
            processing_time=3,
            predicted_processing_time=3.0,
            confidence=0.8,
            deadline=7,
        ),
        Job(
            job_id="job-c",
            release_time=0,
            processing_time=1,
            predicted_processing_time=1.0,
            confidence=0.8,
            deadline=3,
        ),
    ]

    trace = run_policy(EDFPolicy(), jobs, num_machines=1)
    ordered = sorted(trace.scheduled_jobs, key=lambda item: item.start_time)
    for previous, current in zip(ordered, ordered[1:]):
        assert current.start_time >= previous.finish_time
