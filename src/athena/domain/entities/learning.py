"""
src/athena/domain/entities/learning.py
=========================================
Learning domain entities: LearningTopic and LearningCard.

Design rules:
    - Zero external / framework imports.
    - LearningCard carries SM-2 algorithm state; mutation returns new instances
      (handled by MasteryEngine domain service, not the entity itself).
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class DifficultyLevel(str, Enum):
    """Subjective difficulty level assigned to a LearningTopic."""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


@dataclass
class LearningTopic:
    """Represents a subject area the user is actively studying.

    A LearningTopic owns a collection of LearningCards. Mastery progress
    is derived from those cards by the MasteryEngine domain service.

    Attributes
    ----------
    title:
        Short name of the topic (e.g. 'Linear Algebra').
    subject:
        Broader subject area (e.g. 'Mathematics', 'Programming').
    id:
        Globally unique UUID string, auto-generated on creation.
    difficulty:
        Subjective difficulty classification.
    mastery_percentage:
        Float 0.0–100.0 representing how well the user knows this topic.
        Derived and updated by MasteryEngine.
    streak_days:
        Number of consecutive days the user has studied this topic.
    last_studied:
        UTC timestamp of the most recent study session. ``None`` if never.
    created_at:
        UTC timestamp when the topic was first added.
    """

    title: str
    subject: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    mastery_percentage: float = 0.0  # 0.0 – 100.0
    streak_days: int = 0
    last_studied: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def record_study_session(self) -> None:
        """Update last_studied to now and increment streak_days if consecutive.

        Streak is broken if last_studied was more than 1 calendar day ago.
        """
        raise NotImplementedError("record_study_session logic not yet implemented")

    def reset_streak(self) -> None:
        """Reset streak_days to 0 (called when a study day is missed)."""
        raise NotImplementedError("reset_streak logic not yet implemented")

    def update_mastery(self, new_percentage: float) -> None:
        """Overwrite mastery_percentage with a value provided by MasteryEngine.

        Parameters
        ----------
        new_percentage:
            Float in range [0.0, 100.0].

        Raises
        ------
        ValueError
            If *new_percentage* is outside [0.0, 100.0].
        """
        raise NotImplementedError("update_mastery logic not yet implemented")


@dataclass
class LearningCard:
    """A single flashcard associated with a LearningTopic.

    Carries the SuperMemo-2 (SM-2) scheduling state needed by MasteryEngine
    to compute the optimal next review date.

    Attributes
    ----------
    topic_id:
        FK reference to the parent LearningTopic.
    question:
        The prompt shown to the user during review.
    answer:
        The expected correct answer.
    id:
        Globally unique UUID string, auto-generated on creation.
    interval_days:
        Current inter-repetition interval in days (SM-2 parameter *I*).
        Starts at 1 for a new card.
    easiness_factor:
        SM-2 *EF* parameter controlling how quickly interval grows.
        Starts at 2.5; minimum is 1.3 (enforced by MasteryEngine).
    repetitions:
        Number of times this card has been successfully reviewed in a row.
        Resets to 0 on a quality < 3 response.
    next_review_date:
        UTC datetime after which this card is due for another review.
    created_at:
        UTC timestamp when the card was created.
    """

    topic_id: str
    question: str
    answer: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    interval_days: int = 1
    easiness_factor: float = 2.5
    repetitions: int = 0
    next_review_date: datetime = field(default_factory=datetime.utcnow)
    created_at: datetime = field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------ #
    #  Domain behaviour                                                    #
    # ------------------------------------------------------------------ #

    def is_due_for_review(self) -> bool:
        """Return True when the card is ready to be reviewed.

        A card is due when ``datetime.utcnow() >= next_review_date``.

        Returns
        -------
        bool
            ``True`` if the card should be presented to the user now.
        """
        raise NotImplementedError("is_due_for_review logic not yet implemented")

    def days_until_review(self) -> int:
        """Return the number of whole days remaining until next_review_date.

        Returns
        -------
        int
            0 or negative means the card is already due. Positive means it is
            not yet time to review.
        """
        raise NotImplementedError("days_until_review logic not yet implemented")
