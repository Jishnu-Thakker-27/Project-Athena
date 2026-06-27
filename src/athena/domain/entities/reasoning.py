"""
src/athena/domain/entities/reasoning.py
==========================================
ReasoningLog domain entity and DecisionType constants.

Design rules:
    - Zero external / framework imports.
    - DecisionType is a plain class of string constants (not an Enum) so that
      adapters and plugins can extend it without changing domain code.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


class DecisionType:
    """Namespace of well-known decision type string constants.

    Using a plain class instead of an Enum keeps the value set open for
    extension by adapters without modifying domain code.

    Attributes
    ----------
    TASK_PRIORITIZATION:
        Decision about ranking or reordering tasks.
    SCHEDULE_OPTIMIZATION:
        Decision about building or reshuffling the daily schedule.
    GOAL_ALIGNMENT:
        Decision about associating tasks/projects with goals.
    NOTIFICATION_POLICY:
        Decision about whether to deliver or suppress a notification.
    MEMORY_CONSOLIDATION:
        Decision about which memories to promote to long-term storage.
    CAPABILITY_SELECTION:
        Decision about which capability / tool to invoke.
    """

    TASK_PRIORITIZATION: str = "task_prioritization"
    SCHEDULE_OPTIMIZATION: str = "schedule_optimization"
    GOAL_ALIGNMENT: str = "goal_alignment"
    NOTIFICATION_POLICY: str = "notification_policy"
    MEMORY_CONSOLIDATION: str = "memory_consolidation"
    CAPABILITY_SELECTION: str = "capability_selection"

    @classmethod
    def all_known(cls) -> list[str]:
        """Return all string constants defined on this class.

        Returns
        -------
        list[str]
            Every class-level str attribute that does not start with '_'.
        """
        raise NotImplementedError("all_known logic not yet implemented")


@dataclass
class ReasoningLog:
    """Immutable audit record of an AI-driven decision made by Athena.

    Every time an orchestrator or agent makes a non-trivial decision, it
    should persist a ReasoningLog so that the user can inspect *why* a
    particular action was taken.

    Attributes
    ----------
    decision_type:
        Category of decision; use ``DecisionType.*`` constants.
    context_summary:
        Brief description of the inputs / situation that prompted the decision.
    reasoning_text:
        Full chain-of-thought or rationale produced by the model.
    model_used:
        Identifier of the LLM / model that produced the reasoning
        (e.g. ``'gemini-2.5-pro'``).
    id:
        Auto-incrementing placeholder integer. In production this is managed
        by the persistence layer; default of 0 signals "not yet persisted".
    created_at:
        UTC timestamp when the reasoning was recorded.
    confidence_score:
        Optional float 0.0–1.0 expressing model confidence in the decision.
    outcome_description:
        Optional summary of what action was actually taken as a result.
    """

    decision_type: str
    context_summary: str
    reasoning_text: str
    model_used: str
    id: int = field(default=0)  # 0 = not yet persisted; set by repository
    created_at: datetime = field(default_factory=datetime.utcnow)
    confidence_score: float = 0.0  # 0.0 – 1.0
    outcome_description: str = ""

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def is_high_confidence(self, threshold: float = 0.7) -> bool:
        """Return True when confidence_score meets or exceeds the threshold.

        Parameters
        ----------
        threshold:
            Float in [0.0, 1.0]; defaults to 0.7.

        Returns
        -------
        bool
            ``True`` if ``confidence_score >= threshold``.
        """
        raise NotImplementedError("is_high_confidence logic not yet implemented")

    def short_summary(self) -> str:
        """Return a one-line string suitable for audit log output.

        Returns
        -------
        str
            Format: ``[<decision_type>] <truncated context_summary> via <model_used>``.
        """
        raise NotImplementedError("short_summary logic not yet implemented")
