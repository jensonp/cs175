from __future__ import annotations

import random
from typing import List

from scheduler.corruption import apply_prediction_noise
from scheduler.models import Job


def make_bursty_workload(
    *,
    num_jobs: int,
    seed: int,
    deadline_slack: tuple[int, int] = (3, 8),
) -> List[Job]:
    rng = random.Random(seed)
    jobs: List[Job] = []
    burst_centers = [0, 6, 14, 24]

    for index in range(num_jobs):
        burst = burst_centers[index % len(burst_centers)]
        release_time = max(0, burst + rng.randint(0, 4))
        processing_time = rng.randint(1, 7)
        slack = rng.randint(*deadline_slack)
        jobs.append(
            Job(
                job_id=f"job-{index:03d}",
                release_time=release_time,
                processing_time=processing_time,
                predicted_processing_time=float(processing_time),
                confidence=1.0,
                deadline=release_time + processing_time + slack,
                penalty=1.0 + (index % 3) * 0.5,
            )
        )

    jobs.sort(key=lambda job: (job.release_time, job.job_id))
    return apply_prediction_noise(jobs, rng)
