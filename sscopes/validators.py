# -*- coding: utf-8 -*-

from collections import namedtuple
from types import GeneratorType
from functools import lru_cache

from sscopes import exceptions


GLOBAL_NS = "global"
Scope = namedtuple("Scope", ("namespace", "actions", "negations"))


def _normalize(scope):
    """
    Normalizes and returns tuple consisting of namespace, and action(s)
    """
    parts = scope.rsplit("::", 1)
    if len(parts) == 2:
        negations = parts[1].split(":")
        negations = list(filter(lambda v: v, negations))
        if len(negations) == 0:
            negations = None
    else:
        negations = None

    parts = parts[0].split(":")
    return Scope(namespace=parts[0], actions=parts[1:], negations=negations)


def _destructure(scopes):
    """
    Take input of either a space delimited string, or a list-like object and
    return a list of scopes.
    """
    if isinstance(scopes, str):
        return tuple(scopes.split(" "))
    elif isinstance(scopes, (list, tuple, set, GeneratorType)):
        return tuple(scopes)
    else:
        raise exceptions.InvalidScope(
            "Your scopes should either be a string or list-like object"
        )


def _validate_namespace(base_namespace, inbound_namespace):
    """
    Check that the inbound namespace matches against the base namespace
    """
    base_namespace = base_namespace.strip()

    is_global = False if base_namespace and base_namespace != GLOBAL_NS else True

    if is_global:
        return True

    return base_namespace == inbound_namespace


def _validate_actions(base_actions, inbound_actions, require_all_actions=True):
    """
    Check that the inbound actions matches against the base actions
    """
    if base_actions:
        if len(inbound_actions) == 0 or (
            len(base_actions) == 1 and base_actions[0] == ""
        ):
            valid_actions = True
        else:
            method = all if require_all_actions else any
            valid_actions = method(x in inbound_actions for x in base_actions)
    else:
        valid_actions = len(inbound_actions) == 0

    return valid_actions


def _validate_negations(base_negations, inbound_actions):
    """
    Check that the inbound actions do not contain any of the base negations
    """
    if base_negations:
        return all(x not in inbound_actions for x in base_negations)
    return True


@lru_cache(maxsize=256)
def _validate_single_scope(base, inbounds, require_all_actions=True, override=None):
    # Before beginning validaition, return as invalid if inbound is None
    # or is a list containing only None values
    # or if the base is None
    is_valid = False
    do_validation = True

    if not base:
        do_validation = False
    elif not inbounds:
        do_validation = False
    elif inbounds.count(None) > 0:
        if inbounds.count(None) == len(inbounds):
            do_validation = False

        inbounds = list(filter(lambda v: v is not None, inbounds))

    base = _normalize(base)
    inbounds = [_normalize(x) for x in inbounds]

    if not base.namespace and not base.actions and not base.negations:
        do_validation = False

    if do_validation:
        for inbound in inbounds:
            valid_namespace = _validate_namespace(base.namespace, inbound.namespace)
            valid_actions = _validate_actions(
                base.actions, inbound.actions, require_all_actions=require_all_actions
            )
            valid_negations = _validate_negations(base.negations, inbound.actions)

            is_valid = valid_namespace and valid_actions and valid_negations

            # Only one inbound scope needs to match, so we can stop validating
            # after one success
            if is_valid:
                break

    outcome = (
        override(
            is_valid=is_valid,
            base=base,
            inbounds=inbounds,
            require_all_actions=require_all_actions,
        )
        if callable(override)
        else is_valid
    )

    if type(outcome) != bool:
        raise exceptions.OverrideError

    return outcome


def validate(
    base_scopes, inbounds, require_all=True, require_all_actions=True, override=None
):
    # Confirm scopes' formatting
    if any("::::" in x for x in (str(base_scopes), str(inbounds))):
        raise exceptions.InvalidScope

    if inbounds and "::" in inbounds:
        raise exceptions.InvalidScope("Inbound scopes may not contain negations")

    base_scopes = _destructure(base_scopes)
    inbounds = _destructure(inbounds)

    method = all if require_all else any

    return method(
        _validate_single_scope(
            base, inbounds, require_all_actions=require_all_actions, override=override
        )
        for base in base_scopes
    )
