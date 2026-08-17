"""Checkpoint cells: the enforcement mechanism for "no click-through credit."

Where a step genuinely can only be done in the portal (first-run OAuth
consent on a connection, some connection-reference bindings), the notebook
still doesn't just say "go click it". It calls `checkpoint()` with a probe
function that queries for the resulting object. If the probe doesn't find
it, the cell raises with a remediation message and the notebook stops dead
— on purpose. A learner cannot execute the next cell on faith.
"""
from __future__ import annotations

from typing import Callable, TypeVar

T = TypeVar("T")


class CheckpointError(RuntimeError):
    """Raised when a required manual/portal step has not actually been completed."""


def checkpoint(name: str, probe: Callable[[], T], remediation: str) -> T:
    """Run `probe`; on falsy result or exception, raise CheckpointError.

    Parameters
    ----------
    name        Human label for the checkpoint, shown in the error.
    probe       Zero-arg callable that returns a truthy object on success
                (e.g. the connection reference dict, the published agent id).
    remediation Exact steps to complete in the portal/CLI before re-running.
    """
    try:
        result = probe()
    except Exception as exc:  # noqa: BLE001 - we want to wrap *any* probe failure
        raise CheckpointError(
            f"[CHECKPOINT FAILED] {name}\n"
            f"Probe raised: {type(exc).__name__}: {exc}\n\n"
            f"Do this, then re-run this cell:\n{remediation}"
        ) from exc

    if not result:
        raise CheckpointError(
            f"[CHECKPOINT FAILED] {name}\n"
            f"Probe returned nothing.\n\n"
            f"Do this, then re-run this cell:\n{remediation}"
        )

    print(f"[CHECKPOINT OK] {name}")
    return result
