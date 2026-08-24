from runtime.mentor_gateway import MentorLesson, MentorSource, XiaoEMentorGateway, LessonStatus


def build_python_debugging_lesson() -> MentorLesson:
    return MentorLesson(
        lesson_id="mentor-python-debugging-001",
        title="Python Debugging Fundamentals",
        domain="coding",
        objective="Diagnose a reproducible Python defect before changing code.",
        explanation=(
            "Reproduce, isolate, inspect state, form one hypothesis, make the smallest fix, rerun, verify."
        ),
        demonstration="Reproduce an IndexError on [], identify unchecked indexing, add the smallest guard, rerun tests.",
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
        ],
        source=MentorSource(
            mentor_name="ChatGPT",
            provider="OpenAI",
            model="provider-selected",
            delivered_via="xiao_e",
        ),
    )


def test_lesson_requires_practice_and_verification_before_verified():
    gateway = XiaoEMentorGateway()
    lesson = build_python_debugging_lesson()

    decision = gateway.screen(lesson)
    assert decision.accepted_for_practice is True
    assert decision.may_change_identity is False
    assert decision.may_change_authority is False
    assert decision.may_grant_permissions is False

    gateway.mark_practicing(lesson)
    assert lesson.status == LessonStatus.PRACTICING

    gateway.verify(
        lesson,
        passed_checks=[
            "original_failure_reproduced",
            "root_cause_identified",
            "minimal_fix_applied",
            "regression_test_passes",
            "normal_case_still_passes",
        ],
        evidence=["practice-run-001", "regression-suite-pass"],
    )
    assert lesson.status == LessonStatus.VERIFIED
    assert lesson.confidence >= 0.8


def test_protected_domain_is_rejected():
    gateway = XiaoEMentorGateway()
    lesson = build_python_debugging_lesson()
    lesson.domain = "authority"

    decision = gateway.screen(lesson)
    assert decision.accepted_for_practice is False
