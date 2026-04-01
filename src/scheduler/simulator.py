from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import asdict
from typing import Dict, List

from scheduler.meta import MetaScheduler
from scheduler.metrics import summarize_trace
from scheduler.models import DecisionRecord, Job, MachineState, RunTrace, ScheduledJob
from scheduler.policies import ExpertPolicy


def _next_time(current_time: int, pending: Sequence[Job], machines: Sequence[MachineState]) -> int | None:
    next_release = pending[0].release_time if pending else None
    future_machine_times = [machine.available_at for machine in machines if machine.available_at > current_time]
    next_machine = min(future_machine_times) if future_machine_times else None

    candidates = [value for value in (next_release, next_machine) if value is not None]
    return min(candidates) if candidates else None


def run_policy(
    policy: ExpertPolicy | MetaScheduler,
    jobs: Iterable[Job],
    *,
    num_machines: int = 2,
) -> RunTrace:
    pending = sorted(list(jobs), key=lambda job: (job.release_time, job.job_id))
    machines = [MachineState(machine_id=index) for index in range(num_machines)]
    available: List[Job] = []
    current_time = pending[0].release_time if pending else 0
    trace = RunTrace(policy_name=getattr(policy, "name", policy.__class__.__name__), num_machines=num_machines)

    while pending or available:
        while pending and pending[0].release_time <= current_time:
            available.append(pending.pop(0))

        free_machines = [machine for machine in machines if machine.available_at <= current_time]
        while free_machines and available:
            machine = min(free_machines, key=lambda item: item.machine_id)
            if isinstance(policy, MetaScheduler):
                selected_job, selected_expert, weights = policy.choose_job(available, current_time)
                selected_by = selected_expert
            else:
                selected_job = policy.choose_job(available, current_time)
                selected_expert = policy.name
                weights = {policy.name: 1.0}
                selected_by = policy.name

            available.remove(selected_job)
            start_time = current_time
            finish_time = start_time + selected_job.processing_time
            lateness = max(0, finish_time - selected_job.deadline)
            scheduled = ScheduledJob(
                job_id=selected_job.job_id,
                machine_id=machine.machine_id,
                start_time=start_time,
                finish_time=finish_time,
                deadline=selected_job.deadline,
                lateness=lateness,
                missed_deadline=lateness > 0,
                penalty_paid=selected_job.penalty if lateness > 0 else 0.0,
                selected_by=selected_by,
            )
            machine.available_at = finish_time
            trace.scheduled_jobs.append(scheduled)
            trace.decisions.append(
                DecisionRecord(
                    time=current_time,
                    machine_id=machine.machine_id,
                    selected_job_id=selected_job.job_id,
                    selected_policy=trace.policy_name,
                    selected_expert=selected_expert,
                    available_job_ids=[job.job_id for job in sorted(available + [selected_job], key=lambda item: item.job_id)],
                    weight_snapshot=weights,
                )
            )

            if isinstance(policy, MetaScheduler):
                policy.observe_outcome(current_time)

            free_machines = [item for item in machines if item.available_at <= current_time]

        next_time = _next_time(current_time, pending, machines)
        if next_time is None:
            break
        if not available or not [machine for machine in machines if machine.available_at <= current_time]:
            current_time = next_time
        else:
            current_time = min(current_time + 1, next_time)

    return trace


def compare_policies(
    policies: Sequence[ExpertPolicy | MetaScheduler],
    jobs: Sequence[Job],
    *,
    num_machines: int,
) -> Dict[str, Dict[str, float | int | str]]:
    results: Dict[str, Dict[str, float | int | str]] = {}
    for policy in policies:
        trace = run_policy(policy, jobs, num_machines=num_machines)
        results[trace.policy_name] = asdict(summarize_trace(trace))
    return results
