from runtime.activation_command import (
    CANONICAL_ACTIVATION_PHRASE,
    is_xiaoi_activation_command,
)


def test_canonical_xiaoi_activation_phrase():
    assert CANONICAL_ACTIVATION_PHRASE == "小I上线"
    assert is_xiaoi_activation_command("小I上线")


def test_activation_allows_outer_whitespace():
    assert is_xiaoi_activation_command("  小I上线  ")


def test_legacy_phrase_remains_compatible():
    assert is_xiaoi_activation_command("小爱上线")


def test_similar_phrases_do_not_activate():
    assert not is_xiaoi_activation_command("小I 上线啦")
    assert not is_xiaoi_activation_command("小I上线了")
    assert not is_xiaoi_activation_command("现在小I上线")
