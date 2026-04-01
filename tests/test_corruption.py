from __future__ import annotations

import random

from scheduler.corruption import apply_prediction_noise, miscalibrate_confidence
from scheduler.models import Job


def test_prediction_noise_changes_prediction_fields() -> None:
    jobs = [
        Job(
            job_id="job-a",
            release_time=0,
            processing_time=4,
            predicted_processing_time=4.0,
            confidence=1.0,
            deadline=10,
        )
    ]
    noisy = apply_prediction_noise(jobs, random.Random(0), relative_noise=0.2, corruption_rate=1.0)
    assert noisy[0].predicted_processing_time != jobs[0].predicted_processing_time
    assert noisy[0].confidence != jobs[0].confidence


def test_miscalibration_scales_confidence() -> None:
    jobs = [
        Job(
            job_id="job-a",
            release_time=0,
            processing_time=2,
            predicted_processing_time=2.0,
            confidence=0.8,
            deadline=5,
        )
    ]
    shifted = miscalibrate_confidence(jobs, scale=0.5)
    assert shifted[0].confidence == 0.4
