"""
src/athena/domain/entities/project.py
=======================================
Core Project domain entity.

Design rules:
    - Zero external / framework imports.
    - All state transitions are explicit named methods.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ProjectStatus(str, Enum):
    """Lifecycle states a Project can be in."""

    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    ON_HOLD = "on_hold"


@dataclass
class Project:
    """Core project domain entity.

    A Project groups related Tasks and optionally aligns with a Goal.

    Attributes
    ----------
    name:
        Short unique project name.
    id:
        Globally unique UUID string, auto-generated on creation.
    description:
        Optional extended description of the project's purpose.
    status:
        Current lifecycle state (active, completed, archived, on_hold).
    goal_id:
        Optional FK to the parent Goal this project supports.
    priority:
        Integer priority in range 1 (highest) – 5 (lowest).
    deadline:
        Optional UTC datetime by which the project should be delivered.
    created_at:
        UTC timestamp when the project was first created.
    updated_at:
        UTC timestamp of the last mutation; must be refreshed on every change.
    """

    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    status: ProjectStatus = ProjectStatus.ACTIVE
    goal_id: Optional[str] = None
    priority: int = 3  # 1 = highest, 5 = lowest
    deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def archive(self) -> None:
        """Transition the project to ARCHIVED status.

        Once archived, the project is read-only; no tasks should be added.

        Raises
        ------
        ValueError
            If the project is already ARCHIVED.
        """
        raise NotImplementedError("archive logic not yet implemented")

    def activate(self) -> None:
        """Transition the project back to ACTIVE status.

        Useful for un-archiving or resuming an ON_HOLD project.

        Raises
        ------
        ValueError
            If the project is already ACTIVE.
        """
        raise NotImplementedError("activate logic not yet implemented")

    def complete(self) -> None:
        """Mark the project as COMPLETED and update the updated_at timestamp.

        Raises
        ------
        ValueError
            If the project is not currently ACTIVE.
        """
        raise NotImplementedError("complete logic not yet implemented")

    def put_on_hold(self) -> None:
        """Transition the project to ON_HOLD status.

        Raises
        ------
        ValueError
            If the project is not currently ACTIVE.
        """
        raise NotImplementedError("put_on_hold logic not yet implemented")

    def is_overdue(self) -> bool:
        """Return True when the deadline has passed and the project is not COMPLETED.

        Returns
        -------
        bool
            ``True`` if deadline is set, lies in the past, and status != COMPLETED.
        """
        raise NotImplementedError("is_overdue logic not yet implemented")
