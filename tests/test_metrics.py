from __future__ import annotations

from scheduler.metrics import summarize_trace
from scheduler.models import RunTrace, ScheduledJob


def test_metrics_summary_counts_deadline_misses() -> None:
    trace = RunTrace(
        policy_name="edf",
        num_machines=1,
        scheduled_jobs=[
            ScheduledJob(
                job_id="job-a",
                machine_id=0,
                start_time=0,
                finish_time=4,
                deadline=3,
                lateness=1,
                missed_deadline=True,
                penalty_paid=2.5,
                selected_by="edf",
            ),
            ScheduledJob(
                job_id="job-b",
                machine_id=0,
                start_time=4,
                finish_time=5,
                deadline=5,
                lateness=0,
                missed_deadline=False,
                penalty_paid=0.0,
                selected_by="edf",
            ),
        ],
    )

    metrics = summarize_trace(trace)
    assert metrics.total_jobs == 2
    assert metrics.missed_deadlines == 1
    assert metrics.total_penalty == 2.5
    assert metrics.makespan == 5
