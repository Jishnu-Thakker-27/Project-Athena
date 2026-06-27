"""
src/athena/domain/entities/workflow.py
=========================================
Workflow, WorkflowStep, and WorkflowRun domain entities.

Design rules:
    - Zero external / framework imports.
    - The Workflow entity is a pure definition (template); WorkflowRun
      represents a single execution instance of that template.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Literal, Optional


class WorkflowStepStatus(str, Enum):
    """Execution states for an individual step within a WorkflowRun."""

    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStatus(str, Enum):
    """Whether a Workflow definition is currently active (can be triggered)."""

    ACTIVE = "active"
    INACTIVE = "inactive"


class WorkflowRunStatus(str, Enum):
    """Terminal and in-progress states of a single WorkflowRun execution."""

    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


# Type alias for the on_failure policy of a step.
OnFailurePolicy = Literal["continue", "abort", "rollback"]


@dataclass
class WorkflowStep:
    """An individual action step within a Workflow definition.

    Attributes
    ----------
    name:
        Human-readable label for this step (e.g. 'Fetch GitHub Issues').
    action_key:
        Registry key used to look up the Capability handler at runtime.
    id:
        Globally unique UUID string, auto-generated on creation.
    params:
        Key-value parameters passed verbatim to the action handler.
    retry_count:
        Number of automatic retry attempts on transient failure (default 3).
    on_failure:
        Policy executed when the step fails after all retries:
        ``'continue'`` – proceed to next step,
        ``'abort'``    – stop the run and mark it FAILED,
        ``'rollback'`` – execute compensating actions in reverse order.
    timeout_seconds:
        Optional per-step execution timeout; ``None`` means no timeout.
    """

    name: str
    action_key: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    params: dict = field(default_factory=dict)
    retry_count: int = 3
    on_failure: OnFailurePolicy = "abort"
    timeout_seconds: Optional[int] = None


@dataclass
class Workflow:
    """A named, reusable automation definition composed of ordered steps.

    Attributes
    ----------
    name:
        Unique human-readable workflow name.
    trigger_event:
        The event key that causes this workflow to be triggered automatically,
        e.g. ``'task.created'`` or ``'daily.morning'``.
    id:
        Globally unique UUID string, auto-generated on creation.
    description:
        Extended description of what this workflow does.
    steps:
        Ordered list of WorkflowStep objects to be executed in sequence.
    is_active:
        When False, this workflow will not fire even if its event is raised.
    created_at:
        UTC timestamp of workflow definition creation.
    updated_at:
        UTC timestamp of last modification.
    """

    name: str
    trigger_event: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    steps: list[WorkflowStep] = field(default_factory=list)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def activate(self) -> None:
        """Enable this workflow so it responds to trigger events.

        Raises
        ------
        ValueError
            If the workflow is already active.
        """
        raise NotImplementedError("activate logic not yet implemented")

    def deactivate(self) -> None:
        """Disable this workflow; it will be ignored by the event dispatcher.

        Raises
        ------
        ValueError
            If the workflow is already inactive.
        """
        raise NotImplementedError("deactivate logic not yet implemented")

    def add_step(self, step: WorkflowStep, position: Optional[int] = None) -> None:
        """Append or insert a step into the workflow definition.

        Parameters
        ----------
        step:
            The WorkflowStep to add.
        position:
            Zero-based index at which to insert; ``None`` appends to the end.
        """
        raise NotImplementedError("add_step logic not yet implemented")

    def remove_step(self, step_id: str) -> None:
        """Remove a step by its ID.

        Parameters
        ----------
        step_id:
            The UUID of the step to remove.

        Raises
        ------
        KeyError
            If no step with that ID exists.
        """
        raise NotImplementedError("remove_step logic not yet implemented")


@dataclass
class WorkflowRun:
    """A single execution instance of a Workflow.

    Attributes
    ----------
    workflow_id:
        FK reference to the Workflow definition that spawned this run.
    id:
        Globally unique UUID string, auto-generated on creation.
    status:
        Current execution status.
    current_step:
        Zero-based index of the step currently being (or last) executed.
    error_message:
        Human-readable error description; populated on FAILED / ROLLED_BACK.
    start_time:
        UTC timestamp when the run was initiated.
    end_time:
        UTC timestamp when the run terminated (success, failure, or rollback).
        ``None`` while the run is still in progress.
    trigger_payload:
        Optional dict of data that was passed with the triggering event.
    """

    workflow_id: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: WorkflowRunStatus = WorkflowRunStatus.IN_PROGRESS
    current_step: int = 0
    error_message: str = ""
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    trigger_payload: dict = field(default_factory=dict)

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def mark_success(self) -> None:
        """Finalize the run with SUCCESS status and set end_time to now.

        Raises
        ------
        ValueError
            If the run is not currently IN_PROGRESS.
        """
        raise NotImplementedError("mark_success logic not yet implemented")

    def mark_failed(self, error_message: str) -> None:
        """Finalize the run with FAILED status.

        Parameters
        ----------
        error_message:
            Description of what caused the failure.
        """
        raise NotImplementedError("mark_failed logic not yet implemented")

    def mark_rolled_back(self) -> None:
        """Finalize the run as ROLLED_BACK after compensating actions complete."""
        raise NotImplementedError("mark_rolled_back logic not yet implemented")

    def advance_step(self) -> None:
        """Increment current_step by 1."""
        raise NotImplementedError("advance_step logic not yet implemented")

    def is_terminal(self) -> bool:
        """Return True when the run has reached a terminal state.

        Returns
        -------
        bool
            ``True`` for SUCCESS, FAILED, or ROLLED_BACK.
        """
        raise NotImplementedError("is_terminal logic not yet implemented")
