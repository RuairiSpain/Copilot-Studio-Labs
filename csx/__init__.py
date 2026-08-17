"""csx — shared plumbing for the Copilot Studio Enterprise Agent curriculum.

Every notebook imports from here instead of re-implementing auth, client
construction, eval running, or cost accounting. Keep notebooks thin;
put logic here so it is testable and diffable outside of notebook JSON.
"""

from csx.config import Settings, load_settings
from csx.checkpoint import checkpoint, CheckpointError

__all__ = ["Settings", "load_settings", "checkpoint", "CheckpointError"]
