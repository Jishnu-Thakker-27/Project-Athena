"""
src/athena/domain/entities/capability.py
==========================================
Capability domain entity.

Design rules:
    - Zero external / framework imports.
    - The ``handler`` attribute holds a plain Python callable; the domain
      layer does not execute it — that is the responsibility of the
      infrastructure / adapter layer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class Capability:
    """Represents a self-registered agent capability in the Capability Registry.

    Capabilities are the atomic units of functionality that agents can
    discover and invoke. They are registered at startup by adapters and
    plugins, then stored in the CapabilityRegistry (infrastructure layer).

    Attributes
    ----------
    name:
        Unique registry key, e.g. ``'fetch_github_issues'``.
        Must be a valid Python identifier or slug.
    description:
        Human-readable explanation of what this capability does.
        Used by the AI planner to decide which capability to invoke.
    version:
        Semantic version string, e.g. ``'1.0.0'``.
    feature_flag:
        The feature-flag key that must be enabled for this capability to
        be available, e.g. ``'ENABLE_GITHUB_INTEGRATION'``.
    handler:
        The Python callable that executes the capability at runtime.
        Signature: ``handler(**params: Any) -> Any``.
        The domain layer treats this as an opaque callable.
    parameters_schema:
        JSON Schema dict describing the expected ``handler`` keyword
        arguments. Used for validation and LLM function-calling.
    tags:
        Free-form tags for grouping, e.g. ``['github', 'devtools']``.
    is_async:
        ``True`` if the handler is a coroutine function (``async def``).
    timeout_seconds:
        Optional maximum execution time before the runner should cancel.
    """

    name: str
    description: str
    version: str
    feature_flag: str
    handler: Callable[..., Any]
    parameters_schema: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    is_async: bool = False
    timeout_seconds: Optional[int] = None

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def matches_query(self, query: str) -> bool:
        """Return True if *query* appears in the name, description, or tags.

        Used by the capability discovery service to find relevant tools.

        Parameters
        ----------
        query:
            Case-insensitive search string.

        Returns
        -------
        bool
            ``True`` if *query* matches name, description, or any tag.
        """
        raise NotImplementedError("matches_query logic not yet implemented")

    def has_tag(self, tag: str) -> bool:
        """Return True if *tag* is present in this capability's tag list.

        Parameters
        ----------
        tag:
            Exact tag string (case-sensitive).

        Returns
        -------
        bool
            ``True`` if found.
        """
        raise NotImplementedError("has_tag logic not yet implemented")

    def to_llm_tool_spec(self) -> dict:
        """Serialise this capability into an LLM tool-calling specification.

        Returns a dict compatible with the Google Gemini / OpenAI function-
        calling format, using ``name``, ``description``, and
        ``parameters_schema``.

        Returns
        -------
        dict
            LLM-ready tool specification dict.
        """
        raise NotImplementedError("to_llm_tool_spec logic not yet implemented")
