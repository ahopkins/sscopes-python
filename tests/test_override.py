from sscopes import validate
from sscopes import exceptions
from functools import partial
import pytest


def test_override_outcome():
    base = "::"
    inbound = "foo"
    assert validate(base, inbound) is False

    def always_true(**kwargs):
        return True

    assert validate(base, inbound, override=always_true)


def test_override_arguments():
    _base = "::"
    _inbound = "foo"

    def check_args(is_valid, base, inbounds, require_all_actions):
        inbound = inbounds[0]
        return (
            len(inbounds) == 1
            and is_valid is False
            and not base.namespace
            and not base.actions
            and not base.negations
            and inbound.namespace == _inbound
            and not inbound.actions
            and not inbound.negations
            and require_all_actions is False
        )

    assert validate(_base, _inbound, override=check_args, require_all_actions=False)


def test_bad_override_type():
    base = "::"
    inbound = "foo"
    assert validate(base, inbound) is False

    def oops(**kwargs):
        return "foobar"

    def okay(outcome, **kwargs):
        return outcome

    assert validate(base, inbound, override=partial(okay, outcome=True))
    assert not validate(base, inbound, override=partial(okay, outcome=False))

    with pytest.raises(exceptions.OverrideError):
        validate(base, inbound, override=oops)
