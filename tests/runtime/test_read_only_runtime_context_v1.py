from runtime.read_only_runtime_context import ReadOnlyRuntimeContextResolver


class FakeSource:
    def __init__(self):
        self.calls = []

    def resolve_internal_user_id(self, auth_user_id):
        self.calls.append(("resolve_internal_user_id", auth_user_id))
        return "user-1" if auth_user_id == "auth-1" else None

    def resolve_active_access(self, internal_user_id):
        self.calls.append(("resolve_active_access", internal_user_id))
        return {"daughter_id": "daughter-1", "role": "guardian", "authority_scope": "guardian_scope"}

    def resolve_active_chatgpt_client(self, internal_user_id, daughter_id):
        self.calls.append(("resolve_active_chatgpt_client", internal_user_id, daughter_id))
        return {"id": "client-1"}

    def resolve_session(self, internal_user_id, daughter_id, session_key):
        self.calls.append(("resolve_session", internal_user_id, daughter_id, session_key))
        return {"persona_state": "ACTIVE"}

    def resolve_child_name(self, daughter_id):
        self.calls.append(("resolve_child_name", daughter_id))
        return "雨宸"

    def has_visible_continuity(self, internal_user_id, daughter_id, role):
        self.calls.append(("has_visible_continuity", internal_user_id, daughter_id, role))
        return True


def test_resolver_returns_deterministic_snapshot_without_mutation_api():
    source = FakeSource()
    resolver = ReadOnlyRuntimeContextResolver(source)

    snapshot = resolver.resolve(auth_user_id="auth-1", session_key="session-a")

    assert snapshot.resolved is True
    assert snapshot.daughter_id == "daughter-1"
    assert snapshot.internal_user_id == "user-1"
    assert snapshot.role == "guardian"
    assert snapshot.authority_scope == "guardian_scope"
    assert snapshot.client_connection_id == "client-1"
    assert snapshot.persona_state == "ACTIVE"
    assert snapshot.child_name == "雨宸"
    assert snapshot.session_key == "session-a"
    assert snapshot.continuity_visible is True
    assert snapshot.error_code is None

    mutation_names = {"insert", "update", "upsert", "delete", "write", "save", "mutate"}
    exposed = {name for name in dir(source) if not name.startswith("_")}
    assert mutation_names.isdisjoint(exposed)


def test_resolver_fails_closed_when_identity_is_not_bound():
    resolver = ReadOnlyRuntimeContextResolver(FakeSource())
    snapshot = resolver.resolve(auth_user_id="unknown", session_key="s")

    assert snapshot.resolved is False
    assert snapshot.error_code == "identity_not_bound"
    assert snapshot.daughter_id is None
    assert snapshot.continuity_visible is False


def test_resolver_normalizes_empty_session_key_without_promoting_persona():
    source = FakeSource()
    resolver = ReadOnlyRuntimeContextResolver(source)
    snapshot = resolver.resolve(auth_user_id="auth-1", session_key="   ")

    assert snapshot.session_key == "default"
    assert snapshot.persona_state == "ACTIVE"


def test_message_text_is_not_an_input_to_authority_resolution():
    # Resolver API intentionally accepts auth identity + session only. No chat text
    # can claim Guardian/child identity, authority scope, or persona state.
    params = ReadOnlyRuntimeContextResolver.resolve.__annotations__
    assert "message" not in params
