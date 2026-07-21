"""The package must agree with itself about what version it is.

Added 2026-07-21 after an audit found smolagents-colony shipping a version mismatch:
``pyproject.toml`` read 0.9.0 while ``smolagents_colony.__version__`` still read 0.8.0.
PyPI therefore served the correct code under the correct filename, and the
installed package reported the *previous* release at runtime.

That failure is silent by construction. The built artifact takes its version
from pyproject.toml alone, so nothing about the build, the upload or the test
suite is affected -- the package simply lies when asked, and it surfaces weeks
later as a confusing bug report rather than a red build.

The same defect was found the same day in colony-oidc, in the opposite
direction: there ``__init__.py`` was bumped and ``pyproject.toml`` was not,
which made the tagged release unpublishable under its own version number. One
mistake, two directions, three packages. Hence a test rather than a resolution
to be careful.
"""

from __future__ import annotations

import pathlib
import re

import smolagents_colony

ROOT = pathlib.Path(__file__).resolve().parent.parent


def _pyproject_version() -> str:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', text, re.M)
    assert m, "no version field in pyproject.toml"
    return m.group(1)


def test_dunder_version_matches_pyproject() -> None:
    """``__version__`` is what a user observes; pyproject is what ships."""
    assert smolagents_colony.__version__ == _pyproject_version(), (
        f"smolagents_colony.__version__ is {smolagents_colony.__version__!r} but pyproject.toml says "
        f"{_pyproject_version()!r} -- bump BOTH"
    )
