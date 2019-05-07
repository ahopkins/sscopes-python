#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sscopes` package."""

import pytest
from sscopes import validate


@pytest.fixture
def simple_single_specific(ScopeTestCase):
    return (
        ScopeTestCase(base="user", inbound="something", outcome=False),
        ScopeTestCase(base="user", inbound="user", outcome=True),
        ScopeTestCase(base="user", inbound="user:read", outcome=False),
        ScopeTestCase(base="user:read", inbound="user", outcome=True),
        ScopeTestCase(base="user:read", inbound="user:read", outcome=True),
        ScopeTestCase(base="user:read", inbound="user:write", outcome=False),
        ScopeTestCase(base="user:read", inbound="user:read:write", outcome=True),
        ScopeTestCase(base="user:read:write", inbound="user:read", outcome=False),
        ScopeTestCase(base="user:read:write", inbound="user:read:write", outcome=True),
        ScopeTestCase(base="user:read:write", inbound="user:write:read", outcome=True),
        ScopeTestCase(base="user:", inbound="user", outcome=True),
        ScopeTestCase(base="user:", inbound="user:read", outcome=True),
    )


@pytest.fixture
def simple_single_global(ScopeTestCase):
    return (
        ScopeTestCase(base=":", inbound=":read", outcome=True),
        ScopeTestCase(base=":", inbound="admin", outcome=True),
        ScopeTestCase(base=":read", inbound="admin", outcome=True),
        ScopeTestCase(base=":read", inbound=":read", outcome=True),
        ScopeTestCase(base=":read", inbound=":write", outcome=False),
        ScopeTestCase(base="global:", inbound=":read", outcome=True),
        ScopeTestCase(base="global:", inbound="admin", outcome=True),
        ScopeTestCase(base="global:read", inbound="admin", outcome=True),
        ScopeTestCase(base="global:read", inbound=":read", outcome=True),
        ScopeTestCase(base="global:read", inbound=":write", outcome=False),
        ScopeTestCase(base="global", inbound=":read", outcome=False),
        ScopeTestCase(base="global", inbound="admin", outcome=True),
        ScopeTestCase(base="user:write", inbound="global:write", outcome=False),
        ScopeTestCase(base="user:write", inbound=":write", outcome=False),
        ScopeTestCase(base="admin", inbound="global", outcome=False),
    )


@pytest.fixture
def simple_multiple(ScopeTestCase):
    return (
        ScopeTestCase(base="user", inbound="something else", outcome=False),
        ScopeTestCase(base="user", inbound="something else user", outcome=True),
        ScopeTestCase(
            base="user:read", inbound="something:else user:read", outcome=True
        ),
        ScopeTestCase(
            base="user:read", inbound="user:read something:else", outcome=True
        ),
        ScopeTestCase(base="user foo", inbound="user", outcome=False),
        ScopeTestCase(base="user foo", inbound="user foo", outcome=True),
        ScopeTestCase(base="user foo", inbound="foo user", outcome=True),
        ScopeTestCase(base="user:read foo", inbound="user foo", outcome=True),
        ScopeTestCase(base="user:read foo", inbound="user foo:read", outcome=False),
        ScopeTestCase(base="user:read foo", inbound="user:read foo", outcome=True),
        ScopeTestCase(base="user:read foo:bar", inbound=":read :bar", outcome=False),
        ScopeTestCase(base="user:read foo:bar", inbound="user:read foo", outcome=True),
        ScopeTestCase(base="user:read foo:bar", inbound="user foo", outcome=True),
        # Should pass if only one base is required
        ScopeTestCase(base="user foo", inbound="user", outcome=False),
    )


@pytest.fixture
def complex_(ScopeTestCase):
    return (
        ScopeTestCase(base="::delete", inbound="user", outcome=True),
        ScopeTestCase(base="::delete", inbound="user:read", outcome=False),
        ScopeTestCase(base="::delete", inbound="user:delete", outcome=False),
        ScopeTestCase(base="::delete", inbound="user:read:delete", outcome=False),
        ScopeTestCase(base=":::delete", inbound="user", outcome=True),
        ScopeTestCase(base=":::delete", inbound="user:read", outcome=True),
        ScopeTestCase(base=":::delete", inbound="user:delete", outcome=False),
        ScopeTestCase(base=":::delete", inbound="user:read:delete", outcome=False),
        ScopeTestCase(base="user::delete", inbound="user", outcome=True),
        ScopeTestCase(base="user::delete", inbound="user:read", outcome=False),
        ScopeTestCase(base="user::delete", inbound="user:delete", outcome=False),
        ScopeTestCase(base="user::delete", inbound="user:read:delete", outcome=False),
        ScopeTestCase(base="user:::delete", inbound="user", outcome=True),
        ScopeTestCase(base="user:::delete", inbound="user:read", outcome=True),
        ScopeTestCase(base="user:::delete", inbound="user:delete", outcome=False),
        ScopeTestCase(base="user:::delete", inbound="user:read:delete", outcome=False),
        ScopeTestCase(base="user:read::delete", inbound="user", outcome=True),
        ScopeTestCase(base="user:read::delete", inbound="user:read", outcome=True),
        ScopeTestCase(base="user:read::delete", inbound="user:delete", outcome=False),
        ScopeTestCase(
            base="user:read::delete", inbound="user:read:delete", outcome=False
        ),
        ScopeTestCase(base="user:read::delete", inbound="user:write", outcome=False),
        # Should pass if only one base is required
        ScopeTestCase(
            base="user:read user::delete", inbound="user:read:delete", outcome=False
        ),
        ScopeTestCase(
            base="user:read user::delete",
            inbound="user:read user:delete",
            outcome=False,
        ),
        ScopeTestCase(base="", inbound="user", outcome=False),
        ScopeTestCase(base="", inbound=":read", outcome=False),
        ScopeTestCase(base="", inbound="user:read", outcome=False),
        ScopeTestCase(base=" ", inbound="user", outcome=False),
        ScopeTestCase(base=" ", inbound=":read", outcome=False),
        ScopeTestCase(base=" ", inbound="user:read", outcome=False),
        ScopeTestCase(base="::", inbound="user", outcome=False),
        ScopeTestCase(base="::", inbound=":read", outcome=False),
        ScopeTestCase(base="::", inbound="user:read", outcome=False),
    )


def test_regular(
    simple_single_specific, simple_single_global, simple_multiple, complex_
):
    for test_case in (
        simple_single_specific + simple_single_global + simple_multiple + complex_
    ):
        is_valid = validate(test_case.base, test_case.inbound)
        assert is_valid is test_case.outcome


def test_not_require_all(ScopeTestCase):
    assert validate("user foo", "user", require_all=False)
    assert validate("user:read:write", "user:read", require_all_actions=False)

    # from complex_
    assert validate("user:read user::delete", "user:read:delete", require_all=False)
    assert validate(
        "user:read user::delete", "user:read user:delete", require_all=False
    )
