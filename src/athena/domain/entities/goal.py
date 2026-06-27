"""
src/athena/domain/entities/goal.py
=====================================
Core Goal domain entity.

Design rules:
    - Zero external / framework imports.
    - All state transitions are explicit named methods.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Optional


class GoalCategory(str, Enum):
    """High-level life categories a Goal can belong to."""

    CAREER = "career"
    ACADEMIC = "academic"
    HEALTH = "health"
    PERSONAL = "personal"
    FINANCIAL = "financial"


class GoalStatus(str, Enum):
    """Lifecycle states a Goal can occupy."""

    ACTIVE = "active"
    ACHIEVED = "achieved"
    ABANDONED = "abandoned"


@dataclass
class Goal:
    """Core goal domain entity.

    Goals represent high-level intentions that Projects and Tasks align to.

    Attributes
    ----------
    title:
        Concise statement of what the user wants to achieve.
    id:
        Globally unique UUID string, auto-generated on creation.
    description:
        Detailed elaboration of the goal, motivations, and success criteria.
    category:
        Life-area category (career, academic, health, personal, financial).
    status:
        Current lifecycle state.
    target_date:
        Optional calendar date by which the goal should be achieved.
    abandon_reason:
        Populated when the goal is abandoned; describes why it was dropped.
    created_at:
        UTC timestamp when the goal was first created.
    updated_at:
        UTC timestamp of the last mutation.
    """

    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    category: GoalCategory = GoalCategory.PERSONAL
    status: GoalStatus = GoalStatus.ACTIVE
    target_date: Optional[date] = None
    abandon_reason: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def mark_achieved(self) -> None:
        """Transition the goal to ACHIEVED status.

        Refreshes the updated_at timestamp.

        Raises
        ------
        ValueError
            If the goal is not currently ACTIVE.
        """
        raise NotImplementedError("mark_achieved logic not yet implemented")

    def abandon(self, reason: str) -> None:
        """Transition the goal to ABANDONED status.

        Parameters
        ----------
        reason:
            Non-empty string explaining why the goal is being abandoned.
            Stored in the ``abandon_reason`` attribute.

        Raises
        ------
        ValueError
            If *reason* is empty or the goal is already ABANDONED / ACHIEVED.
        """
        raise NotImplementedError("abandon logic not yet implemented")

    def is_past_target(self) -> bool:
        """Return True when a target_date is set and lies in the past.

        Returns
        -------
        bool
            ``True`` if target_date is set and today is after it.
        """
        raise NotImplementedError("is_past_target logic not yet implemented")
