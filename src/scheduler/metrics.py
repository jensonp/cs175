from __future__ import annotations

from scheduler.models import MetricsSummary, RunTrace


def summarize_trace(trace: RunTrace) -> MetricsSummary:
    total_jobs = len(trace.scheduled_jobs)
    if total_jobs == 0:
        return MetricsSummary(
            policy_name=trace.policy_name,
            total_jobs=0,
            missed_deadlines=0,
            total_penalty=0.0,
            average_lateness=0.0,
            makespan=0,
            machine_utilization=0.0,
        )

    total_penalty = sum(job.penalty_paid for job in trace.scheduled_jobs)
    total_lateness = sum(job.lateness for job in trace.scheduled_jobs)
    missed = sum(1 for job in trace.scheduled_jobs if job.missed_deadline)
    makespan = max(job.finish_time for job in trace.scheduled_jobs)
    busy_time = sum(job.finish_time - job.start_time for job in trace.scheduled_jobs)
    utilization = busy_time / max(1, makespan * trace.num_machines)

    return MetricsSummary(
        policy_name=trace.policy_name,
        total_jobs=total_jobs,
        missed_deadlines=missed,
        total_penalty=float(total_penalty),
        average_lateness=float(total_lateness) / total_jobs,
        makespan=makespan,
        machine_utilization=utilization,
    )
