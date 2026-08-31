"""Coldline — Task 1.4.

===================

File:              tests/contract/test_submission.py
Component:         Contract tests — Test Submission
Purpose:           Tests for the public answer and path checks for this Task's submission.
Interacts With:    Published interfaces and repository boundaries
Sprint/Task:       Sprint 1 — Project 1 / Task 1.4
Concepts:          Compatibility, ownership, export safety
Tools:             Python 3.12, pytest
"""

from pathlib import Path

import pytest
import yaml

from tests.contract.submission_validation import (
    SubmissionError,
    main,
    validate_changed_paths,
    validate_submission,
)

ROOT = Path(__file__).parents[2]


def valid_answers() -> dict[str, object]:
    """Return a complete fictional answer sheet unrelated to Coldline outcomes."""
    return {
        "answers": {
            "baseline_run_1": (
                "Fictional baseline run 1 reached 48 fictional requests per second with "
                "fictional p95 latency of 150 fictional milliseconds and a fictional peak "
                "queue backlog of 12 fictional messages."
            ),
            "baseline_run_2": (
                "Fictional baseline run 2 reached 49 fictional requests per second with "
                "fictional p95 latency of 148 fictional milliseconds and a fictional peak "
                "queue backlog of 11 fictional messages."
            ),
            "repeatability_notes": (
                "The two fictional baseline runs stayed within a fictional 2 percent "
                "throughput band, so the fictional baseline is repeatable."
            ),
            "latency_injected_run": (
                "Injecting 300 fictional milliseconds into the fictional model provider "
                "raised fictional worker duration but only dropped fictional throughput "
                "from 48 to 46 fictional requests per second."
            ),
            "bottleneck_analysis": (
                "Fictional worker CPU utilization stayed above 90 percent while fictional "
                "queue backlog grew steadily before the fictional model provider's response "
                "time changed, pointing to fictional worker concurrency as the first resource "
                "to saturate under the tested fictional workload."
            ),
            "alternative_elimination": (
                "The fictional latency-injection run reduced fictional throughput by only "
                "about 4 percent, far less than expected if the fictional provider were the "
                "binding constraint, so the fictional report's claim is not supported."
            ),
        }
    }


def test_complete_answer_shape_passes_public_validation(tmp_path: Path) -> None:
    """A complete direct-answer mapping must pass syntax and schema validation."""
    submission = tmp_path / "submission.yaml"
    submission.write_text(yaml.safe_dump(valid_answers()), encoding="utf-8")

    validate_submission(submission, ROOT / "docs/contracts/submission.schema.json")


def test_blank_template_fails_with_field_address(tmp_path: Path) -> None:
    """An untouched answer sheet must identify an incomplete field."""
    submission = tmp_path / "submission.yaml"
    submission.write_text((ROOT / "submission.yaml").read_text(encoding="utf-8"), encoding="utf-8")

    with pytest.raises(SubmissionError, match="answers.baseline_run_1"):
        validate_submission(submission, ROOT / "docs/contracts/submission.schema.json")


def test_malformed_yaml_is_rejected(tmp_path: Path) -> None:
    """A syntactically invalid answer sheet must fail safely."""
    submission = tmp_path / "submission.yaml"
    submission.write_text("answers: [unterminated", encoding="utf-8")

    with pytest.raises(SubmissionError, match="valid YAML"):
        validate_submission(submission, ROOT / "docs/contracts/submission.schema.json")


def test_unexpected_answer_field_is_rejected(tmp_path: Path) -> None:
    """Fields outside the published direct-answer schema must fail validation."""
    answers = valid_answers()
    answer_mapping = answers["answers"]
    assert isinstance(answer_mapping, dict)
    answer_mapping["repair_hint"] = "not part of this Task's schema"
    submission = tmp_path / "submission.yaml"
    submission.write_text(yaml.safe_dump(answers), encoding="utf-8")

    with pytest.raises(SubmissionError, match="Additional properties"):
        validate_submission(submission, ROOT / "docs/contracts/submission.schema.json")


def test_exact_sample_copy_is_rejected(tmp_path: Path) -> None:
    """The fictional sample must not be accepted as a student submission."""
    submission = tmp_path / "submission.yaml"
    submission.write_text(
        (ROOT / "submission-sample.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    with pytest.raises(SubmissionError, match="fictional sample"):
        validate_submission(
            submission,
            ROOT / "docs/contracts/submission.schema.json",
            sample_path=ROOT / "submission-sample.yaml",
        )


def test_only_student_editable_paths_are_permitted() -> None:
    """The advisory path gate must accept this Task's editable paths and reject others."""
    validate_changed_paths(
        [
            "submission.yaml",
            "loadtest/model_provider_latency.py",
        ]
    )

    with pytest.raises(SubmissionError, match="src/api"):
        validate_changed_paths(["src/api/routes.py"])


def test_public_entrypoint_reports_an_incomplete_answer_sheet(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Catch a verifier entrypoint that skips the real submission contract."""
    (tmp_path / "docs/contracts").mkdir(parents=True)
    (tmp_path / "submission.yaml").write_text(
        (ROOT / "submission.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "submission-sample.yaml").write_text(
        (ROOT / "submission-sample.yaml").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (tmp_path / "docs/contracts/submission.schema.json").write_text(
        (ROOT / "docs/contracts/submission.schema.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    assert main(tmp_path, changed_paths=[]) == 1
    assert "answers.baseline_run_1 is incomplete" in capsys.readouterr().err
