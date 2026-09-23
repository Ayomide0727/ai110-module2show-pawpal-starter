"""
PawPal+ system classes.

Skeleton only — names, attributes, and empty method stubs matching
diagrams/uml.mmd. No scheduling logic implemented yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, grooming, enrichment, etc.)."""

    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    start_time: time | None = None
    reason: str = ""


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def edit_task(self, task_id, changes: dict) -> None:
        pass


@dataclass
class Owner:
    """The pet owner using the app."""

    name: str
    available_minutes_per_day: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass


@dataclass
class Scheduler:
    """Builds a daily plan for a pet's tasks given an owner's constraints."""

    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)

    def generate_plan(self, pet: Pet, owner: Owner) -> None:
        pass

    def explain(self) -> str:
        pass
