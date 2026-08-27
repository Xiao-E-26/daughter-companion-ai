def evaluate_scope(scope, requested_identity):
    requested_identity = (requested_identity or "xiaoai").lower()
    namespace = str(scope.get("identity_namespace", "xiaoai")).lower()
    allowed = [str(x).lower() for x in scope.get("allowed_identities", [])]
    denied = [str(x).lower() for x in scope.get("denied_identities", [])]
    cross_project_access = scope.get("cross_project_access") is True

    if requested_identity in denied:
        return 403, "identity_scope_denied"
    if requested_identity != namespace and not cross_project_access:
        return 403, "cross_project_identity_denied"
    if allowed and requested_identity not in allowed:
        return 403, "identity_not_allowed"
    if requested_identity != "xiaoai":
        return 403, "unsupported_identity"
    return 200, "ok"


def mother_scope():
    return {
        "memory_access": False,
        "runtime_control": False,
        "requires_identity_binding": True,
        "identity_namespace": "xiaoai",
        "allowed_identities": ["xiaoai"],
        "denied_identities": ["xiaoe"],
        "cross_project_access": False,
    }


def test_mother_can_resolve_xiaoai():
    assert evaluate_scope(mother_scope(), "xiaoai") == (200, "ok")


def test_mother_cannot_resolve_xiaoe():
    assert evaluate_scope(mother_scope(), "xiaoe") == (403, "identity_scope_denied")


def test_mother_cannot_cross_project_by_alias():
    assert evaluate_scope(mother_scope(), "voucher") == (403, "cross_project_identity_denied")


def test_default_identity_is_xiaoai():
    assert evaluate_scope(mother_scope(), None) == (200, "ok")
