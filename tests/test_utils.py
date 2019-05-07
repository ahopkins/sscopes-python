from sscopes.validators import _normalize


def test_negation_normalizing():
    scope = "user:read:write::delete"
    normalized = _normalize(scope)

    assert normalized.namespace == "user"
    assert len(normalized.actions) == 2
    assert len(normalized.negations) == 1
