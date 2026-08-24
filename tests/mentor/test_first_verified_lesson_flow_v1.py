from runtime.lesson_store import LessonStore
from runtime.mentor_gateway import LessonStatus, MentorLesson, MentorSource, XiaoEMentorGateway
from runtime.practice_runner import PracticeAttempt, PracticeRunner


def build_python_debugging_lesson() -> MentorLesson:
    return MentorLesson(
        lesson_id="mentor-python-debugging-001",
        title="Python Debugging Fundamentals",
        domain="coding",
        objective="Diagnose a reproducible Python defect before changing code.",
        explanation=(
            "Reproduce the failure, isolate the smallest failing case, inspect state, form one hypothesis, "
            "change one variable, rerun, and verify the fix."
        ),
        demonstration=(
            "For an empty-list IndexError, reproduce with [], identify unchecked index access, add the "
            "smallest correct guard, then rerun the failing and normal cases."
        ),
        practice_tasks=[
            "Fix an IndexError without changing unrelated behavior.",
            "Explain root cause separately from symptom.",
            "Add a regression test for the original failure.",
        ],
        verification_checks=[
            "original_failure_reproduced",
            "root_cause_identified",
            "minimal_fix_applied",
            "regression_test_passes",
            "normal_case_still_passes",
        ],
        reusable_principles=[
            "Reproduce before patching.",
            "Prefer root-cause fixes over symptom masking.",
            "Change one variable at a time when debugging.",
            "Verify both the former failure and unaffected behavior.",
        ],
        source=MentorSource(
            mentor_name="ChatGPT",
            provider="OpenAI",
            model="provider-selected",
            delivered_via="xiao_e",
        ),
    )


def test_practice_failure_then_correction_then_verified():
    store = LessonStore()
    runner = PracticeRunner(XiaoEMentorGateway(), store)
    lesson = runner.begin(build_python_debugging_lesson())

    assert lesson.status == LessonStatus.PRACTICING
    assert store.reusable_principles("coding") == []

    first_attempt = PracticeAttempt(
        lesson_id=lesson.lesson_id,
        passed_checks=[
            "original_failure_reproduced",
            "root_cause_identified",
            "minimal_fix_applied",
        ],
        evidence=[
            "Reproduced IndexError on empty list.",
            "Identified direct access to index 0 without empty-list guard.",
            "Applied a narrow empty-input guard.",
        ],
        notes=["First attempt forgot regression coverage and unaffected normal-case verification."],
    )
    first = runner.submit(first_attempt)

    assert first.status == LessonStatus.PRACTICING
    assert first.reusable is False
    assert set(first.missing_checks) == {"regression_test_passes", "normal_case_still_passes"}
    assert store.reusable_principles("coding") == []

    corrected_attempt = PracticeAttempt(
        lesson_id=lesson.lesson_id,
        passed_checks=[
            "original_failure_reproduced",
            "root_cause_identified",
            "minimal_fix_applied",
            "regression_test_passes",
            "normal_case_still_passes",
        ],
        evidence=[
            "Added regression test for empty input.",
            "Regression test passes after fix.",
            "Normal non-empty behavior still passes.",
        ],
        notes=["Corrected missing verification instead of lowering the standard."],
    )
    second = runner.submit(corrected_attempt)

    assert second.status == LessonStatus.VERIFIED
    assert second.reusable is True
    assert second.missing_checks == []
    assert second.confidence >= 0.8

    principles = store.reusable_principles("coding")
    assert "Reproduce before patching." in principles
    assert "Prefer root-cause fixes over symptom masking." in principles


def test_unverified_lesson_cannot_be_reused():
    store = LessonStore()
    runner = PracticeRunner(XiaoEMentorGateway(), store)
    runner.begin(build_python_debugging_lesson())

    assert store.list_verified() == []
    assert store.reusable_principles() == []
