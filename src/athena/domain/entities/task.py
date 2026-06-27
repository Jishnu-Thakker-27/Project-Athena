"""
src/athena/domain/entities/task.py
====================================
Core Task domain entity.

Design rules:
    - Zero external / framework imports.
    - All state changes go through explicit methods so that domain events
      can be emitted by use-case callers.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(str, Enum):
    """Lifecycle states a Task can occupy."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class TaskPriority(int, Enum):
    """Numeric priority levels (lower value = higher urgency)."""

    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    MINIMAL = 5


@dataclass
class Task:
    """Core task domain entity. Framework-free.

    Attributes
    ----------
    title:
        Short human-readable title.
    id:
        Globally unique UUID string, auto-generated on creation.
    description:
        Optional detailed description of the task.
    status:
        Current lifecycle status.
    priority:
        Urgency/importance level; lower int = higher urgency.
    project_id:
        Optional FK to the owning Project entity.
    goal_id:
        Optional FK to the aligned Goal entity.
    due_date:
        Optional UTC deadline for the task.
    created_at:
        UTC timestamp when the task was first created.
    updated_at:
        UTC timestamp of the last mutation; must be refreshed on every change.
    """

    title: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    project_id: Optional[str] = None
    goal_id: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def mark_done(self) -> None:
        """Mark this task as completed and refresh the updated_at timestamp.

        Raises
        ------
        ValueError
            If the task is already in DONE status.
        """
        raise NotImplementedError("mark_done logic not yet implemented")

    def reprioritize(self, new_priority: TaskPriority) -> None:
        """Update task priority and refresh the updated_at timestamp.

        Parameters
        ----------
        new_priority:
            The replacement priority level.

        Raises
        ------
        ValueError
            If *new_priority* is the same as the current priority.
        """
        raise NotImplementedError("reprioritize logic not yet implemented")

    def start(self) -> None:
        """Transition the task from TODO → IN_PROGRESS."""
        raise NotImplementedError("start logic not yet implemented")

    def block(self, reason: str = "") -> None:
        """Transition the task to BLOCKED state.

        Parameters
        ----------
        reason:
            Optional human-readable description of what is blocking progress.
        """
        raise NotImplementedError("block logic not yet implemented")

    def is_overdue(self) -> bool:
        """Return True when due_date is set and lies in the past.

        Returns
        -------
        bool
            ``True`` if the task has a due date and it has already passed.
        """
        raise NotImplementedError("is_overdue logic not yet implemented")
