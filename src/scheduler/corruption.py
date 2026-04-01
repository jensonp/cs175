from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import replace
from typing import List

from scheduler.models import Job


def apply_prediction_noise(
    jobs: Iterable[Job],
    rng: random.Random,
    relative_noise: float = 0.15,
    corruption_rate: float = 0.1,
) -> List[Job]:
    corrupted: List[Job] = []
    for job in jobs:
        noise = rng.uniform(-relative_noise, relative_noise)
        predicted = max(1.0, job.processing_time * (1.0 + noise))
        confidence = max(0.05, 1.0 - abs(noise))
        if rng.random() < corruption_rate:
            predicted = max(1.0, job.processing_time * rng.uniform(1.6, 2.4))
            confidence = rng.uniform(0.05, 0.4)
        corrupted.append(
            replace(
                job,
                predicted_processing_time=round(predicted, 2),
                confidence=round(min(1.0, confidence), 3),
            )
        )
    return corrupted


def miscalibrate_confidence(jobs: Iterable[Job], scale: float = 0.75) -> List[Job]:
    adjusted: List[Job] = []
    for job in jobs:
        adjusted.append(replace(job, confidence=round(max(0.0, min(1.0, job.confidence * scale)), 3)))
    return adjusted
