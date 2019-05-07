import pytest
from sscopes import validate
from sscopes.exceptions import InvalidScope


def test_list_scopes():
    base = ["foo", "bar"]
    inbound = "foo"
    assert validate(base, inbound) is False

    inbound = "foo bar"
    assert validate(base, inbound)

    inbound = "foo", "bar"
    assert validate(base, inbound)


def test_dict_scopes():
    base = {"foo": "bar"}
    inbound = "foo"

    with pytest.raises(InvalidScope):
        assert validate(base, inbound)


def test_none_input():
    base = "foo"
    inbound = []
    assert validate(base, inbound) is False

    inbound = [None, None]
    assert validate(base, inbound) is False

    inbound = [None, "foo"]
    assert validate(base, inbound)


def test_none_scopes():
    base = None
    inbound = "bar"
    with pytest.raises(InvalidScope):
        validate(base, inbound)

    base = "foo"
    inbound = None
    with pytest.raises(InvalidScope):
        validate(base, inbound)


def test_inbound_negation():
    base = "foo"
    inbound = "::bar"
    with pytest.raises(InvalidScope):
        validate(base, inbound)


def test_overzealous_colons():
    base = "foo::::bar"
    inbound = "bar"
    with pytest.raises(InvalidScope):
        validate(base, inbound)


def test_negation_without_specifc_actions():
    base = "foo::bar"
    inbound = "foo"

    assert validate(base, inbound)
