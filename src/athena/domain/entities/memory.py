"""
src/athena/domain/entities/memory.py
=======================================
Core Memory domain entity.

Design rules:
    - Zero external / framework imports.
    - Memories are immutable snapshots; summarization returns a new string,
      not a mutated object.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MemoryType(str, Enum):
    """Semantic classification of what a memory represents."""

    USER_FACT = "user_fact"
    """A persistent fact about the user, e.g. 'User is allergic to peanuts'."""

    ENTITY_FACT = "entity_fact"
    """A fact about an external entity, e.g. 'Project X deadline is Q3'."""

    CHAT_SUMMARY = "chat_summary"
    """Condensed summary of a single conversation session."""

    DAILY_SUMMARY = "daily_summary"
    """End-of-day distillation of all working-memory from that day."""


class MemoryTier(str, Enum):
    """Storage tier determining retrieval urgency and retention policy."""

    WORKING = "working"
    """Ephemeral within-session context; discarded or consolidated daily."""

    DAILY = "daily"
    """Persisted across the current day; reviewed by the nightly consolidator."""

    LONG_TERM = "long_term"
    """Durable facts stored indefinitely; subject to active forgetting policy."""


@dataclass
class Memory:
    """Core memory domain entity.

    Represents a single unit of retained information across Athena's memory
    tiers. Memories are produced by agents and consumed by the memory
    consolidator and retrieval services.

    Attributes
    ----------
    content:
        The raw text content of the memory.
    id:
        Globally unique UUID string, auto-generated on creation.
    type:
        Semantic classification of the memory.
    tier:
        Storage tier that governs retention and retrieval.
    tags:
        Free-form list of string tags for similarity search and filtering.
    source_agent:
        Optional identifier of the agent that created this memory.
    importance_score:
        Float 0.0–1.0 representing how important/relevant this memory is.
        Higher means more likely to survive consolidation.
    created_at:
        UTC timestamp when the memory was recorded.
    """

    content: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MemoryType = MemoryType.USER_FACT
    tier: MemoryTier = MemoryTier.WORKING
    tags: list[str] = field(default_factory=list)
    source_agent: str = ""
    importance_score: float = 0.5  # 0.0 – 1.0
    created_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def summarize(self) -> str:
        """Return a compact single-line string representation of this memory.

        Intended for use when building LLM prompts that reference multiple
        memories without overwhelming the context window.

        Returns
        -------
        str
            A concise description: ``[<type>] <truncated content>``.
        """
        raise NotImplementedError("summarize logic not yet implemented")

    def with_tier(self, new_tier: MemoryTier) -> Memory:
        """Return a new Memory instance promoted/demoted to *new_tier*.

        Memories are treated as value-like; this returns a new object
        rather than mutating in place.

        Parameters
        ----------
        new_tier:
            The target storage tier.

        Returns
        -------
        Memory
            A copy of this memory with the tier field updated.
        """
        raise NotImplementedError("with_tier logic not yet implemented")

    def matches_tags(self, query_tags: list[str]) -> bool:
        """Return True if any of *query_tags* intersect with this memory's tags.

        Parameters
        ----------
        query_tags:
            Tags to search for.

        Returns
        -------
        bool
            ``True`` if at least one tag matches.
        """
        raise NotImplementedError("matches_tags logic not yet implemented")
